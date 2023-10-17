import re
from components.Knowledge_graph import Knowledge_graph
from dataset.Dataset import Dataset, Entry
from components.Question import Question
from components.Language import Language


class LCquad2(Dataset):
    def __init__(self, lcquad2_file, is_predicted=False) -> None:
        self.is_predicted = is_predicted
        self.entries = self.build_lcquad2_list(lcquad2_file)
        self.knowledge_graph = Knowledge_graph.Wikidata

    def build_lcquad2_list(self, lcquad_file: list):
        lcquad_list = []
        for lcquad in lcquad_file:
            lcquad_entry = LCquad2_entry(
                lcquad["uid"],
                lcquad["NNQT_question"],
                "en",
                lcquad["sparql_wikidata"],
                Knowledge_graph.Wikidata
            )
            lcquad_list.append(lcquad_entry)
        return lcquad_list


class LCquad2_entry(Entry):
    def __init__(self, uid, NNQT_question, language, sparql, knowledge_graph) -> None:
        self.uid = uid
        self.question = self.build_question(NNQT_question, language)
        self.query = super().build_query(sparql, knowledge_graph)

    def build_question(self, NNQT_question, language):
        question_string = self.preprocess_nnqt_question(NNQT_question)
        return Question(question_string, Language(language))
    
    def preprocess_nnqt_question(self, NNQT_ques):
        NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))
        NNQT_ques = re.sub(' +', ' ', NNQT_ques)
        return NNQT_ques.strip()

