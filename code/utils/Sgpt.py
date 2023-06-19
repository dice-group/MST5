from utils.query import ask_dbpedia
from utils.qald import build_qald_entry
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


class Sgpt:
    def __init__(self, queries: list) -> None:
        self.queries: list = self.convert_file_to_Sgpt_entries(queries)
        self.add_answers()
        self.ref_qald: list = []
        self.pred_qald: list = []

    def convert_file_to_Sgpt_entries(self, queries: list) -> list:
        entries: list = list()
        for q in queries:
            entry = Sgpt_entry(q["ground_truth_sparql"], q["predicted_sparql"])
            entries.append(entry)
        return entries

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

class Sgpt_entry:
    def __init__(self, ref_query: str, pred_query: str) -> None:
        self.ref_query: str = ref_query
        self.pred_query: str = pred_query

    def add_prefixes(self, query: str) -> str:
        return (' ').join(prefixes) + query
    
    def get_answer(self, query: str) -> dict:
        query_with_prefixes = self.add_prefixes(query)
        return ask_dbpedia(query_with_prefixes)