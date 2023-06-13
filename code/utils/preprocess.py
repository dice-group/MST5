import re
import json

prefix_abbr = [
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

symbol_replacement = [
    ['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', 'rdf:type'],
    ['{', ' bra_open '],
    ['}', ' bra_close '],
    ['\?', ' var_'],
    [':', '_'],
    ['\.(?!\d)', ' sep_dot '],
    ['\|', ' sep_or '],
]


def read_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def delete_sparql_prefix(sparql_query):
    if "prefix" not in sparql_query.casefold():
        return sparql_query
    elif "ASK" in sparql_query:
        return "ASK" + sparql_query.split("ASK", 1)[1]
    elif "SELECT" in sparql_query:
        return "SELECT" + sparql_query.split("SELECT", 1)[1]
    return sparql_query


def replace_prefix_abbr(sparql_query):
    for prefix in prefix_abbr:
        sparql_query = re.sub(prefix[0], prefix[1]+r'\1', sparql_query)
    for symbol in symbol_replacement:
        sparql_query = re.sub(symbol[0], symbol[1], sparql_query)
    sparql_query = re.sub(' +', ' ', sparql_query)
    return sparql_query


def preprocess_nnqt_question(NNQT_ques):
    # Remove all specified characters
    NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))

    # Replace multiple spaces with a single space
    NNQT_ques = re.sub(' +', ' ', NNQT_ques)

    return NNQT_ques
