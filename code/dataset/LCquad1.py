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

    
    def export_csv(self, output_file, include_linguistic_context=False, include_entity_knowledge=False):
        csv_dataset = self.to_csv(include_linguistic_context, include_entity_knowledge)
        export_csv(output_file, csv_dataset)
        
    def to_csv(self, include_linguistic_context=False, include_entity_knowledge=False):
        csv = [['question', 'query']]
        entry: LCquad1Entry
        for entry in self.entries:
            question = entry.question
            question_string = question.question_string
            if include_linguistic_context:
                question_string = self.add_linguistic_context(question, question_string)
            if include_entity_knowledge:
                question_string = self.add_entity_knowledge(entry, question_string)
            sparql = entry.query.preprocess()
            csv.append([question_string, sparql])
        return csv

    def add_linguistic_context(self, question, question_string):
        _, pos, dep, depth_list = question.get_linguistic_context()
        question_string += " <pad> " + " ".join(pos) \
                    + " <pad> " + " ".join(dep) \
                    + " <pad> " + " ".join(map(str, depth_list))
        return question_string

    def add_entity_knowledge(self, entry, question_string):
        entity_knowledge = entry.query.get_entity_knowledge()
        question_string += " <pad> " + " ".join(entity_knowledge)
        return question_string


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