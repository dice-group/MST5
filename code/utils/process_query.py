import re

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


def delete_sparql_prefix(sparql_query):
    if "prefix" not in sparql_query.lower():
        return sparql_query
    elif "ASK" in sparql_query:
        return "ASK" + split_query_after_keyword(sparql_query, "ASK")
    elif "SELECT" in sparql_query:
        return "SELECT" + split_query_after_keyword(sparql_query, "SELECT")
    return sparql_query

def split_query_after_keyword(sparql_query, keyword):
    return sparql_query.split(keyword, 1)[1]


def replace_prefix_abbr(sparql_query):
    for prefix in PREFIX_ABBR:
        sparql_query = re.sub(prefix[0], prefix[1]+r'\1', sparql_query)
    for symbol in SYMBOL_REPLACEMENT:
        sparql_query = re.sub(symbol[0], symbol[1], sparql_query)
    sparql_query = re.sub(' +', ' ', sparql_query)
    return sparql_query


def preprocess_nnqt_question(NNQT_ques):
    # Remove all specified characters
    NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))

    # Replace multiple spaces with a single space
    NNQT_ques = re.sub(' +', ' ', NNQT_ques)

    return NNQT_ques


def preprocess_sparql(sparql_query):
    return replace_prefix_abbr(
        delete_sparql_prefix(sparql_query))


def postprocess_sparql(sparql_query):
    for r in REPLACEMENT_BACK:
        if r[0] in sparql_query:
            sparql_query = sparql_query.replace(r[0], r[1])
    return sparql_query
