from typing import Dict

def build_qald_entry(id, question_string, sparql_query, answer, language):
    # id-Object
    entry_id = {"id": id}
    
    # question-Object
    entry_question = {"question": [
        {"language": language, "string": question_string}]}

    # query-Object
    entry_query = {"query": {"sparql": sparql_query}}

    # answers-Object
    entry_answers: Dict = {"answers": [answer]}

    # Combined-Object
    qald_entry = {
        "id": entry_id["id"],
        "question": entry_question["question"],
        "query": entry_query["query"],
        "answers": entry_answers["answers"],
    }

    return qald_entry