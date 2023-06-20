from typing import Dict
from utils.process_query import preprocess_sparql


def build_qald_entry(id, question_string, sparql_query, answer, language):
    entry_id = {"id": id}

    entry_question = {"question": [
        {"language": language, "string": question_string}]}

    entry_query = {"query": {"sparql": sparql_query}}

    entry_answers: Dict = {"answers": [answer]}

    qald_entry = {
        "id": entry_id["id"],
        "question": entry_question["question"],
        "query": entry_query["query"],
        "answers": entry_answers["answers"],
    }

    return qald_entry


def build_question_string_with_linguistic(question):
    return " ".join(question["doc"]) \
        + " <pad> " + " ".join(question["pos"]) \
        + " <pad> " + " ".join(question["dep"]) \
        + " <pad> " + " ".join(map(str, question["dep_depth"]))


def get_question_query_list(data, languages, linguistic):
    question_query_list = [['question', 'query']]

    qald_list = data["questions"]

    for qald_entry in qald_list:
        for lang_ques_dict in qald_entry["question"]:
            query = preprocess_sparql(qald_entry["query"]["sparql"])
            if lang_ques_dict["language"] in languages:
                if linguistic:
                    ques_str = build_question_string_with_linguistic(
                        lang_ques_dict)
                else:
                    ques_str = lang_ques_dict["string"]
                question_query_list.append([ques_str, query])
    return question_query_list
