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

class Query:
    def __init__(self, sparql: str, knowledge_graph: Knowledge_graph) -> None:
        self.sparql = self.postprocess_sparql(sparql)
        self.knowledge_graph = knowledge_graph

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


    def postprocess_sparql(self, sparql):
        for r in REPLACEMENT_BACK:
            if r[0] in sparql:
                sparql = sparql.replace(r[0], r[1])
        return sparql
    
    
    def get_answer(self):
        if self.knowledge_graph == Knowledge_graph.DBpedia:
            answer = self.ask_dbpedia()
        elif self.knowledge_graph == Knowledge_graph.Wikidata:
            answer = self.ask_wikidata()
        return answer
    
    def ask_dbpedia(self) -> dict[str, any]:
        try:
            sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
            sparql.setReturnFormat(JSON)
            sparql.setQuery(self.sparql)
            return sparql.query().convert()
        except SPARQLWrapperException as exception:
            return {"head": {"vars": []}, "results": {"bindings": []}}

    def ask_wikidata(self):
        endpoint_url = "https://query.wikidata.org/sparql"
        try:
            user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
            sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
            sparql.setQuery(self.sparql)
            sparql.setReturnFormat(JSON)
            return sparql.query().convert()
        except:
            return {"head": {"vars": []}, "results": {"bindings": []}}
        
        
    def get_entity_knowledge(self) -> list:
        if self.knowledge_graph==Knowledge_graph.DBpedia:
            pattern = r'\b(dbr_\w+|res_\w+)\b'
        elif self.knowledge_graph==Knowledge_graph.Wikidata:
            pattern = r'\bwd_\w+\b'
        entities = re.findall(pattern, self.preprocess())
        return entities
    
    def get_en_uri(self):
        response = self.ask_dbpedia()
        return response["results"]["bindings"][0]["uri"]["value"]
