import re
import sys
from components.Knowledge_graph import Knowledge_graph
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import SPARQLWrapperException


REPLACEMENT_BACK = [
    ["var-", " ?"],
    ["var_", " ?"],
    ["var=", " ?"],
    ["var ", " ?"],
    ["var _", " ?"],
    ["bra_open", " { "],
    ["bra_close", " } "],
    ["bra-close", " } "],
    ["sep_dot", "."],
    ["sep_or", "|"],
    ["res_", "dbr:"],
    ["dbo_", "dbo:"],
    ["dbp_", "dbp:"],
    ["dbr_", "dbr:"],
    ["pq_", "pq:"],
    ["ps_", "ps:"],
    ["dct_", "dct:"],
    ["yago_", "yago:"],
    ["onto_", "onto:"],
    ["rdf_type", "rdf:type"],
    ["wd_", "wd:"],
    ["wdt_", "wdt:"],
    ["p_", "p:"],
    ["psv_", "psv:"],
    ["wikibase_", "wikibase:"],
    ["rdfs_label", "rdfs:label"],
    ["xsd_integer", "xsd:integer"],
    ["__a", "_:a"]
]

PREFIX_ABBR = [
    [r'<http://dbpedia.org/resource/(.*?)>\.?', 'dbr:'],
    [r'<http://dbpedia.org/property/(.*?)>\.?', 'dbp:'],
    [r'<http://dbpedia.org/ontology/(.*?)>\.?', 'dbo:'],
    [r'<http://dbpedia.org/class/yago/(.*?)>\.?', 'yago:'],
    [r'onto:(.*)', 'dbo:'],
    [r'<http://www.wikidata.org/prop/direct/(.*?)>', 'wdt:'],
    [r'<http://www.wikidata.org/prop/statement/(.*?)>\.?', 'ps:'],
    [r'<http://www.wikidata.org/prop/qualifier/(.*?)>\.?', 'pq:'],
    [r'<http://www.wikidata.org/entity/(.*?)>', 'wd:'],
    [r'http://www.wikidata.org/prop/(.*?)', 'p:'],
    [r'<http://www.w3.org/2000/01/rdf-schema#(.*?)', 'rdfs:'],
]

SYMBOL_REPLACEMENT = [
    ['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', 'rdf:type'],
    ['{', ' bra_open '],
    ['}', ' bra_close '],
    ['\?', ' var_'],
    [':', '_'],
    ['\.(?!\d)', ' sep_dot '],
    ['\|', ' sep_or '],
]

QUERY_PREFIX_WIKIDATA = """
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX wdv: <http://www.wikidata.org/value/>
"""

QUERY_PREFIX_DBPEDIA = """
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

ANSWER_LIMIT = 1000

## Dbpedia Endpoint
DBP_SPARQL_ENDPOINT = "http://dbpedia.org/sparql/"
#DBP_ENDPOINT = "http://dbpedia.org/sparql/"
## Wikidata Endpoint
#WD_ENDPOINT =  "https://query.wikidata.org/sparql"
WD_SPARQL_ENDPOINT = "https://skynet.coypu.org/wikidata/"

class Query:
    def __init__(self, sparql: str, knowledge_graph: Knowledge_graph, is_predicted=False) -> None:
        self.is_predicted = is_predicted
        self.knowledge_graph = knowledge_graph
        self.sparql = self.postprocess_sparql(sparql)

    def preprocess(self):
        return self.replace_prefix_abbr(
            self.delete_sparql_prefix(self.sparql))
    
    def replace_prefix_abbr(self, sparql):
        for prefix in PREFIX_ABBR:
            sparql = re.sub(prefix[0], prefix[1]+r'\1', sparql)
        for symbol in SYMBOL_REPLACEMENT:
            sparql = re.sub(symbol[0], symbol[1], sparql)
        sparql = re.sub(' +', ' ', sparql)
        return sparql
    
    def delete_sparql_prefix(self, sparql):
        if "prefix" not in sparql.lower():
            return sparql
        elif "ASK" in sparql:
            return "ASK" + self.split_query_after_keyword(sparql, "ASK")
        elif "SELECT" in sparql:
            return "SELECT" + self.split_query_after_keyword(sparql, "SELECT")
        return sparql
    
    def split_query_after_keyword(self, sparql_query, keyword):
        return sparql_query.split(keyword, 1)[1]


    def postprocess_sparql(self, sparql: str):
        for r in REPLACEMENT_BACK:
            if r[0] in sparql:
                sparql = sparql.replace(r[0], r[1])
        if self.is_predicted:
            query_prefix = ''
            if self.knowledge_graph == Knowledge_graph.DBpedia:
                query_prefix = QUERY_PREFIX_DBPEDIA
            elif self.knowledge_graph == Knowledge_graph.Wikidata:
                query_prefix = QUERY_PREFIX_WIKIDATA
            sparql = query_prefix + '\n' + sparql
        return sparql
    
    
    def get_answer(self):
        if self.knowledge_graph == Knowledge_graph.DBpedia:
            query_exec_info = self.ask_dbpedia()
        elif self.knowledge_graph == Knowledge_graph.Wikidata:
            query_exec_info = self.ask_wikidata()
        return query_exec_info
    
    def ask_dbpedia_old(self) -> dict[str, any]:
        try:
            sparql = SPARQLWrapper(DBP_SPARQL_ENDPOINT)
            sparql.setReturnFormat(JSON)
            sparql.setQuery(self.sparql)
            return sparql.query().convert()
        except SPARQLWrapperException as exception:
            return {"head": {"vars": []}, "results": {"bindings": []}}
        
    def ask_kg(self, endpoint_url):
        query_exec_info = {
            'empty_endpoint_result': False,
            'sparql_exception': False,
            'answer': None
        }

        try:
            if not (self.sparql or self.sparql.strip()):
                raise Exception("SPARQL string is empty.")
            #user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
            #sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(self.sparql)
            # print('Executing:', self.sparql)
            sparql.setReturnFormat(JSON)
            sparql.setTimeout(600)
            sparql_results = sparql.query().convert()
            # check if the results are too big
            if "results" in sparql_results and "bindings" in sparql_results["results"]:
                bindings = sparql_results["results"]["bindings"]
                if len(bindings) > ANSWER_LIMIT:
                    raise Exception("SPARQL result surpasses the set answer limit: %d" % ANSWER_LIMIT)
                elif len(bindings) == 0:
                    query_exec_info['empty_endpoint_result'] = True
            else:
                query_exec_info['empty_endpoint_result'] = True
            # return extracted results
            query_exec_info['answer'] = sparql_results          
            return query_exec_info
        except Exception as e:
            print('Exception occurred for \tSPARQL: %s' % (self.sparql))
            print(str(e))
            query_exec_info['sparql_exception'] = True
            query_exec_info['answer'] = {"head": {"vars": []}, "results": {"bindings": []}}  
            return query_exec_info

    def ask_dbpedia(self):
        endpoint_url = DBP_SPARQL_ENDPOINT
        return self.ask_kg(endpoint_url)
    
    def ask_wikidata(self):
        endpoint_url = WD_SPARQL_ENDPOINT
        return self.ask_kg(endpoint_url)
        
        
    def get_entity_knowledge(self) -> list:
        if self.knowledge_graph==Knowledge_graph.DBpedia:
            pattern = r'\b(dbr_\w+|res_\w+)\b'
        elif self.knowledge_graph==Knowledge_graph.Wikidata:
            pattern = r'\bwd_\w+\b'
        entities = re.findall(pattern, self.preprocess())
        return entities
    
    def get_en_uri(self):
        response = self.ask_dbpedia_old()
        return response["results"]["bindings"][0]["uri"]["value"]
