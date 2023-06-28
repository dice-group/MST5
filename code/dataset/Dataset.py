from components.Query import Query
from components.Question import Question

class Dataset:
    def __init__(self, entries: list[Query]):
        self.entries = entries

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
