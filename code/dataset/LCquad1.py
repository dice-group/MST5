from dataset.Dataset import Dataset, Entry
from components.Query import Query
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from utils.data_io import export_csv

class LCquad1(Dataset):
    def __init__(self, entries):
        self.entries: list[LCquad1Entry] = []
        self.parse_entries(entries)

    def parse_entries(self, entries):
        for entry in entries:
            self.entries.append(LCquad1Entry(entry))

    def to_csv(self):
        csv = [['question', 'query']]
        for entry in self.entries:
            question_string = entry.question.question_string
            sparql = entry.query.sparql
            csv.append([question_string, sparql])
        return csv
    
    def export_csv(self, output_file):
        csv_dataset = self.to_csv()
        export_csv(output_file, csv_dataset)
        


class LCquad1Entry(Entry):
    def __init__(self, lcquad1_entry):
        self.question = self.get_question_from_input_query(lcquad1_entry)
        self.query = self.get_query_from_input_entry(lcquad1_entry)

    def get_query_from_input_entry(self, entry):
        sparql = entry["sparql_query"]
        return Query(sparql, Knowledge_graph.DBpedia)
    
    def get_question_from_input_query(self, entry):
        question_string = entry["corrected_question"]
        return Question(question_string, Language.en)