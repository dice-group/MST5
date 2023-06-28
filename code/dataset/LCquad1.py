from dataset.Dataset import Dataset, Entry
from components.Query import Query
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language

class LCquad1(Dataset):
    def __init__(self, entries):
        self.entries = entries


class LCquad1Entry(Entry):
    def __init__(self, lcquad1_entry):
        
        self.question = Question("", Language.en)
        self.query = Query("", Knowledge_graph.DBpedia)

    def get_query_from_input_entry(self, entry):
        sparql = entry["sparql_query"]
        return Query(sparql, Knowledge_graph.DBpedia)
    
