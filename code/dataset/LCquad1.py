from dataset.Dataset import Dataset, Entry
from components.Query import Query
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from utils.data_io import export_csv

class LCquad1(Dataset):
    def __init__(self, entries):
        self.entries: list[LCquad1_entry] = []
        self.parse_entries(entries)

    def parse_entries(self, entries):
        for entry in entries:
            self.entries.append(LCquad1_entry(entry))

            

class LCquad1_entry(Entry):
    def __init__(self, lcquad1_entry):
        self.question = self.build_question_from_input_query(lcquad1_entry)
        self.query = super().build_query(lcquad1_entry["sparql_query"], Knowledge_graph.DBpedia)
    
    def build_question_from_input_query(self, entry):
        question_string = entry["corrected_question"]
        return Question(question_string, Language.en)