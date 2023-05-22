import re
import json

prefix_pattern = [
    [r'<http://dbpedia.org/resource/(.*?)>\.?', 'dbr:'],
    [r'<http://dbpedia.org/property/(.*?)>\.?', 'dbp:'],
    [r'<http://dbpedia.org/ontology/(.*?)>\.?', 'dbo:'],
    [r'<http://dbpedia.org/class/yago/(.*?)>\.?', 'yago:'],
    [r'onto:(.*)', 'dbo:'],
    [r'<http://www.wikidata.org/prop/direct/(.*?)>', 'wdt:'],
    [r'<http://www.wikidata.org/prop/statement/(.*?)>\.?'],
    [r'<http://www.wikidata.org/prop/qualifier/(.*?)>\.?']
    [r'<http://www.wikidata.org/entity/(.*?)>', 'wd:'],
    [r'http://www.wikidata.org/prop/(.*?)', 'p:'],
    [r'<http://www.w3.org/2000/01/rdf-schema#(.*?)', 'rdfs:'],
]

replacement = [
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
    if "ASK" in sparql_query:
        return "ASK" + sparql_query.split("ASK", 1)[1]
    return "SELECT" + sparql_query.split("SELECT", 1)[1]


def replace_prefix_abbr(sparql_query):
    for pattern in prefix_pattern:
        sparql_query = re.sub(pattern[0], pattern[1]+r'\1', sparql_query)
    for replace in replacement:
        sparql_query = re.sub(replace[0], replace[1], sparql_query)
    sparql_query = re.sub(' +', ' ', sparql_query)
    return sparql_query
