from components.Knowledge_graph import Knowledge_graph
from utils.data_io import export_csv
from dataset.Dataset import Dataset, Entry
from components.Question import Question
from components.Query import Query
from components.Language import Language
import re


class LCquad2(Dataset):
    def __init__(self, lcquad_file) -> None:
        self.entries = self.build_lcquad2_list(lcquad_file)

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

    def export_train_csv(self, output_file, include_linguistic_context: bool = False, include_entity_knowledge: bool = False):
        csv_dataset = [["question", "query"]]
        lcquad_entry: LCquad2_entry
        for lcquad_entry in self.entries:
            query = lcquad_entry.preprossed_query
            question = lcquad_entry.get_question_string(
                include_linguistic_context, include_entity_knowledge)
            csv_dataset.append([question, query])
        export_csv(output_file, csv_dataset)


class LCquad2_entry(Entry):
    def __init__(self, uid, NNQT_question, language, sparql, knowledge_graph) -> None:
        self.uid = uid
        self.question = self.build_question(NNQT_question, language)
        self.query = self.build_query(sparql, knowledge_graph)

    def build_question(self, NNQT_question, language):
        question_string = self.preprocess_nnqt_question(NNQT_question)
        return Question(question_string, Language(language))
    
    def build_query(self, sparql, knowledge_graph):
        return Query(sparql, knowledge_graph)

    def get_question_string(self, include_linguistic_context, include_entity_knowledge) -> str:
        question_string = self.NNQT_question
        if include_linguistic_context:
            question_string += self.get_linguistic_context_string()
        if include_entity_knowledge:
            question_string += self.get_entity_knowledge()
        return question_string

    def preprocess_nnqt_question(self, NNQT_ques):
        NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))
        NNQT_ques = re.sub(' +', ' ', NNQT_ques)
        return NNQT_ques.strip()
