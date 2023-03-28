import json
import time
from typing import Dict
from query import ask_dbpedia, ask_wikidata

def build_qald_entry(id, question_string, sparql_query, answer, language):
    # id-Object
    json_id = {"id": id}

    # question-Object
    json_question = {"question": [
        {"language": language, "string": question_string}]}

    # query-Object
    json_query = {"query": {"sparql": sparql_query}}

    # answers-Object
    json_answers: Dict = {"answers": [answer]}

    # Combined-Object
    qald_question_entry = {
        "id": json_id["id"],
        "question": json_question["question"],
        "query": json_query["query"],
        "answers": json_answers["answers"],
    }

    return qald_question_entry

def export_json(data):
    t = time.strftime("%m.%d.%Y_%H:%M")
    file_name = "gerbil_eval_" + t + ".json"
    f = open(file_name, 'w+', encoding='utf-8')
    json.dump(data, f, ensure_ascii=False, indent=4)
    print("json file is exported in " + file_name)
