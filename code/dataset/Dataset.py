from components.Query import Query
from components.Question import Question
from utils.data_io import export_csv

class Dataset:
    def __init__(self, entries: list[Query]):
        self.entries = entries

    def export_train_csv(self, output_file, include_linguistic_context=False, include_entity_knowledge=False):
        csv_dataset = self.to_train_csv(include_linguistic_context, include_entity_knowledge)
        export_csv(output_file, csv_dataset)

    def to_train_csv(self, include_linguistic_context=False, include_entity_knowledge=False):
        csv = [['question', 'query']]
        entry: Entry
        for entry in self.entries:
            question = entry.question
            question_string = self.get_question_string(include_linguistic_context, include_entity_knowledge, entry, question)
            sparql = entry.query.preprocess()
            csv.append([question_string, sparql])
        return csv

    def get_question_string(self, include_linguistic_context: bool, include_entity_knowledge: bool, entry, question: Question):
        question_string = question.question_string
        if include_linguistic_context:
            question_string = question.get_question_string_with_lingtuistic_context()
        if include_entity_knowledge:
            entity_knowledge = entry.query.get_entity_knowledge()
            question_string = question.add_entity_knowledge(question_string, entity_knowledge)
        return question_string

class Entry:
    def __init__(self, question: Question, query: Query):
        self.question = question
        self.query = query
