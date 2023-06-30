from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from components.Query import Query
from components.Question import Question
from utils.data_io import export_csv

class Dataset:
    def __init__(self, entries: list[Query], knowledge_graph=None):
        self.entries = entries
        self.knowledge_graph = knowledge_graph

    def export_train_csv(self, output_file, include_linguistic_context=False, include_entity_knowledge=False):
        csv_dataset = self.to_train_csv(include_linguistic_context, include_entity_knowledge)
        export_csv(output_file, csv_dataset)

    def to_train_csv(self, include_linguistic_context=False, include_entity_knowledge=False):
        csv = [['question', 'query']]
        entry: Entry
        for entry in self.entries:
            question = entry.question
            question_string = self.get_question_string(entry, question, include_linguistic_context, include_entity_knowledge)
            sparql = entry.query.preprocess()
            csv.append([question_string, sparql])
        return csv

    def get_question_string(self, entry, question: Question, include_linguistic_context: bool, include_entity_knowledge: bool, pred=False):
        question_string = question.question_string
        if include_linguistic_context:
            question_string = question.get_question_string_with_lingtuistic_context()
        if include_entity_knowledge:
            if pred:
                if self.is_kg_wikidata():
                    entity_knowledge = self.get_wikidata_entities(entry, question)
                elif self.is_kg_dbpedia():
                    entity_knowledge = self.get_dbpedia_entities(question)
            else:
                entity_knowledge = entry.query.get_entity_knowledge()

            question_string = question.add_entity_knowledge(question_string, entity_knowledge)
        return question_string

    def is_kg_wikidata(self):
        return self.knowledge_graph==Knowledge_graph.Wikidata

    def is_kg_dbpedia(self):
        return self.knowledge_graph==Knowledge_graph.DBpedia
    
    def get_wikidata_entities(self, entry, question):
        ner = Language.get_supported_ner(question.language)
        if self.no_supported_ner(ner):
            entity_knowledge = entry.questions["en"].recognize_entities("babelscape_ner", "mgenre_el")
        else:
            entity_knowledge = question.recognize_entities(ner, "mgenre_el")
        return entity_knowledge
    
    def no_supported_ner(self, ner):
        return ner=="no_ner"


    def get_dbpedia_entities(self, question: Question):
        return question.recognize_entities("babelscape_ner" ,"mag_el")
    


class Entry:
    def __init__(self, question: Question, query: Query):
        self.question = question
        self.query = query

    def build_query(self, sparql, knowledge_graph):
        return Query(sparql, knowledge_graph)

    def build_qald_format_entry(self, qid, question_lang_and_string, sparql, answers):
        qald_format_entry = {
            "id": qid,
            "question": question_lang_and_string,
            "query": {"sparql": sparql},
            "answers": [answers],
        }

        return qald_format_entry
