from dataset.Dataset import Dataset, Entry
from components.Language import Language
from components.Question import Question
from components.Query import Query
from utils.data_io import export_json

prefixes = [
    "PREFIX dbo: <http://dbpedia.org/ontology/>"
    "PREFIX dbp: <http://dbpedia.org/property/>",
    "PREFIX dbc: <http://dbpedia.org/resource/Category:>",
    "PREFIX dbr: <http://dbpedia.org/resource/>",
    "PREFIX dct: <http://purl.org/dc/terms/>",
    "PREFIX res: <http://dbpedia.org/resource/>",
    "PREFIX prop: <http://dbpedia.org/property/>",
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
    "PREFIX onto: <http://dbpedia.org/ontology/>",
    "PREFIX dbpedia2: <http://dbpedia.org/property/>",
    "PREFIX yago: <http://dbpedia.org/class/yago/>",
    "PREFIX foaf:<http://xmlns.com/foaf/0.1/>",
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>",
    "PREFIX owl: <http://www.w3.org/2002/07/owl#>",
    "PREFIX db: <http://dbpedia.org/>",
]


class Sgpt_pred(Dataset):
    def __init__(self, sgpt_pred_file: list, knowledge_graph) -> None:
        self.entries = self.build_sgpt_list(sgpt_pred_file, knowledge_graph)

    def build_sgpt_list(self, sgpt_pred_file, knowledge_graph):
        entries = []
        for entry in sgpt_pred_file:
            entries.append(Sgpt_entry(entry, knowledge_graph))
        return entries
    
    def to_ref_qald(self):
        entry: Sgpt_entry
        for entry in self.entries:
            entry.ref_query.sparql

    def build_and_extract_ref_qald(self, output_file) -> None:
        self.build_ref_qald()
        qald = {"questions": self.ref_qald}
        export_json(output_file, qald)


    def build_ref_qald(self) -> None:
        id: int
        entry: Sgpt_entry
        for id, entry in enumerate(self.queries):
            answer = entry.get_answer(entry.ref_query)
            self.ref_qald.append(build_qald_entry(
                id, "example question", entry.ref_query, answer, "en"))

    def build_and_extract_pred_qald(self, output_file) -> None:
        self.build_pred_qald()
        qald = {"questions": self.pred_qald}
        export_json(output_file, qald)

    def build_pred_qald(self) -> None:
        id: int
        entry: Sgpt_entry
        for id, entry in enumerate(self.queries):
            answer = entry.get_answer(entry.pred_query)
            self.pred_qald.append(build_qald_entry(
                id, "example question", entry.pred_query, answer, "en"))



class Sgpt_entry(Entry):
    def __init__(self, entry, knowledge_graph) -> None:
        self.ref_query: Query = super().build_query(entry["ground_truth_sparql"], knowledge_graph)
        self.pred_query: Query = super().build_query(entry["predicted_sparql"], knowledge_graph)

    def build_qald_format_entry(self, id, source):
        if source=="ref":
            query = self.ref_query
        elif source=="pred":
            query = self.pred_query
        else:
            raise ValueError("Invalid source")
        question_lang_and_string = {
                        "language": "en",
                        "string": "example question"
                    }
        
        answer = query.get_answer()
        
        return super().build_qald_format_entry(id, question_lang_and_string, query.sparql, answer)

    def add_prefixes(self, query: str) -> str:
        return (' ').join(prefixes) + query

    def get_answer(self, query: str) -> dict:
        query_with_prefixes = self.add_prefixes(query)
        return ask_dbpedia(query_with_prefixes)


def build_sgpt_dict(sgpt_set):
    sgpt_dict = dict()
    for entry in sgpt_set:
        sgpt_dict[entry["en_ques"]] = entry
    return sgpt_dict


def is_question_in_sgpt(question_string, sgpt_set):
    return question_string in sgpt_set


def export_sgpt_file(output, sgpt_set):
    sgpt_train = [v for v in sgpt_set.values()]
    export_json(output, sgpt_train)


def change_sparql(sgpt_dict, qald_entry, question_string):
    fil_sparql = postprocess_sparql(
        preprocess_sparql(qald_entry["query"]["sparql"]))
    sgpt_dict[question_string]["fil_sparql"] = fil_sparql


def change_dbpedia_sparql_to_sparql(wikidata_qald, sgpt_dbpedia, output):
    sgpt_dict = build_sgpt_dict(sgpt_dbpedia)
    qald_entries = wikidata_qald["questions"]
    for qald_entry_wikidata in qald_entries:
        for question in qald_entry_wikidata["question"]:
            if question["language"] == "en":
                question_string = question["string"].lower()
                if is_question_in_sgpt(question_string, sgpt_dict):
                    change_sparql(sgpt_dict, qald_entry_wikidata,
                                  question_string)
    export_sgpt_file(output, sgpt_dict)
