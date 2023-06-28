from dataset.Dataset import Dataset, Entry
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language

class LCquad1(Dataset):
    def __init__(self, lcquad1_file):
        self.entries: list[LCquad1_entry] = self.build_lcquad1_list(lcquad1_file)

    def build_lcquad1_list(self, lcquad1_file):
        entries = []
        for entry in lcquad1_file:
            entries.append(LCquad1_entry(entry))
        return entries
    

class LCquad1_entry(Entry):
    def __init__(self, lcquad1_entry):
        self.question = self.build_question_from_input_query(lcquad1_entry)
        self.query = super().build_query(lcquad1_entry["sparql_query"], Knowledge_graph.DBpedia)
    
    def build_question_from_input_query(self, entry):
        question_string = entry["corrected_question"]
        return Question(question_string, Language.en)