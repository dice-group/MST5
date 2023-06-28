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

    
    def export_train_csv(self, output_file, include_linguistic_context=False, include_entity_knowledge=False):
        csv_dataset = self.to_train_csv(include_linguistic_context, include_entity_knowledge)
        export_csv(output_file, csv_dataset)
        
    def to_train_csv(self, include_linguistic_context=False, include_entity_knowledge=False):
        csv = [['question', 'query']]
        entry: LCquad1_entry
        for entry in self.entries:
            question = entry.question
            question_string = super().get_question_string(include_linguistic_context, include_entity_knowledge, entry, question)
            sparql = entry.query.preprocess()
            csv.append([question_string, sparql])
        return csv
    


class LCquad1_entry(Entry):
    def __init__(self, lcquad1_entry):
        self.question = self.build_question_from_input_query(lcquad1_entry)
        self.query = self.build_query_from_input_entry(lcquad1_entry)

    def build_query_from_input_entry(self, entry):
        sparql = entry["sparql_query"]
        return Query(sparql, Knowledge_graph.DBpedia)
    
    def build_question_from_input_query(self, entry):
        question_string = entry["corrected_question"]
        return Question(question_string, Language.en)