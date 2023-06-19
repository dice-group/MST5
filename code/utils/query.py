import requests
from transformers import pipeline
from typing import Dict, Any
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import SPARQLWrapperException


def init_summarizer(checkpoint_path):
    return pipeline("summarization", model=checkpoint_path, max_length=128, device=1)


def predict_query(summarizer, question_string):
    return summarizer(question_string)[0]['summary_text']


def ask_wikidata(sparql_query):
    try:
        r = requests.get('https://query.wikidata.org/sparql',
                         params={'format': 'json', 'query': sparql_query})
        return r.json()
    except:
        return {"head": {"vars": []}, "results": {"bindings": []}}


def ask_dbpedia(sparql_query: str) -> Dict[str, Any]:
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        return sparql.query().convert()
    except SPARQLWrapperException as exception:
        return {"head": {"vars": []}, "results": {"bindings": []}}
