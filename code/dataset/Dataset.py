from components.Query import Query
from components.Question import Question

class Dataset:
    def __init__(self, entries: list[Query]):
        self.entries = entries

class Entry:
    def __init__(self, question: Question, query: Query):
        self.question = question
        self.query = query
