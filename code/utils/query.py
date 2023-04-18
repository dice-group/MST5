import requests
from transformers import pipeline
from typing import Dict, Any
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.SPARQLExceptions import SPARQLWrapperException


def init_summarizer(checkpoint_path):
    return pipeline("summarization", model=checkpoint_path, max_length=128)

def predict_query(summarizer, question_string):
    return summarizer(question_string)[0]['summary_text']

def ask_wikidata(sparql_query):
    url = 'https://query.wikidata.org/sparql'
    try:
        r = requests.get(url, params={'format': 'json', 'query': sparql_query})
        return r.json()
    except:
        return {"answers": [{"head": {"vars": []}, "results": {"bindings": []}}]}


def ask_dbpedia(question: str, sparql_query: str, lang: str) -> Dict[str, Any]:
    """Send a SPARQL-query to DBpedia and return a formated QALD-string containing the answers.

    Parameters
    ----------
    question : str
        Natural language question asked by an enduser.
    sparql_query : str
        SPARQL-query to be sent to DBpedia. Should correspond to the question.
    lang : str
        Language tag for the question (should always be "en").

    Returns
    -------
    qald_answer : str
        Formated string in the QALD-format containing the answers for the sparql_query.
    """
    # print("SPARQL-Query:", sparql_query.encode("utf-8"))

    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        return sparql.query().convert()
    except SPARQLWrapperException as exception:
        return {"answers": [{"head": {"vars": []}, "results": {"bindings": []}}]}
