from utils.data_io import *
from dataset.Dataset import Dataset, Entry
from components.Language import Language
from components.Question import Question
from components.Query import Query


class Qald(Dataset):
    def __init__(self, qald_file: dict={}, knowledge_graph=None) -> None:
        self.entries = self.build_qald_list(qald_file, knowledge_graph)

    def build_qald_list(self, qald_dataset: dict, knowledge_graph) -> list:
        qald_list = []
        if qald_dataset:
            dataset = qald_dataset["questions"]
            for entry in dataset:
                qald_entry = Qald_entry(entry["id"], entry["question"], entry["query"]["sparql"], knowledge_graph, entry["answers"])
                qald_list.append(qald_entry)
        return qald_list
    
    def add_entry(self, id, language, question_string, sparql, knowledge_graph, answers=None):
        question = Question(question_string, Language[language])
        query = Query(sparql, knowledge_graph)
        self.entries.append(Qald_entry(id, question, query, answers))


    def export_train_csv(self, output_file, languages, include_linguistic_context=False, include_entity_knowledge=False) -> None:
        csv_dataset = self.to_train_csv(languages, include_linguistic_context, include_entity_knowledge)
        export_csv(output_file, csv_dataset)

    def to_train_csv(self, languages, include_linguistic_context, include_entity_knowledge):
        csv_dataset = [["question", "query"]]
        entry: Qald_entry
        for entry in self.entries:
            sparql = entry.query.preprocess()
            for language in languages:
                if language in entry.questions:
                    question: Question = entry.questions[language]
                    question_string = super().get_question_string(include_linguistic_context, include_entity_knowledge, entry, question)
                    csv_dataset.append([question_string, sparql])
        return csv_dataset


    def export_qald_json(self, languages: list, output: str) -> None:
        qald_entries: list = []
        qald_entry: Qald_entry
        for qald_entry in self.entries:
            qald_entries.append(qald_entry.build_qald_format_entry(languages))
        export_json(output, {"questions": qald_entries})


    def get_id_question_list(self, language, include_linguistic_context: bool = False, include_entity_knowledge: bool = False) -> list:
        questions_with_id = []
        entry: Qald_entry
        for entry in self.entries:
            if language in entry.questions:
                question: Question = entry.questions[language]
                question_string = super().get_question_string(include_linguistic_context, include_entity_knowledge, entry, question)
                questions_with_id.append([entry.id, question_string])
        return questions_with_id
    

    def update_answers(self):
        qald_entry: Qald_entry
        for qald_entry in self.entries:
            qald_entry.update_answer()



class Qald_entry(Entry):
    def __init__(self, id, questions, sparql, knowledge_graph, answers=None) -> None:
        self.id = id
        self.questions: dict[Question] = self.build_questions(questions)
        self.query: Query = self.build_query(sparql, knowledge_graph)
        self.answers = answers

    def build_questions(self, questions: list[dict]) -> dict:
        entry_questions = {}
        for q in questions:
            entry_questions[q["language"]] = Question(q["string"], Language[q["language"]])
        return entry_questions
    
    def build_query(self, sparql, knowledge_graph):
        return Query(sparql, knowledge_graph)


    def get_entity_knowledge(self) -> list:
        return self.query.get_entity_knowledge()


    def build_qald_format_entry(self, languages: list) -> dict:
        entry_id = {"id": self.id}

        question_lang_and_string = self.get_question_lang_and_strings(languages)

        entry_question = {
            "question": question_lang_and_string
        }

        entry_query = {"query": {"sparql": self.query.sparql}}

        entry_answers: dict = {"answers": [self.answers]}

        qald_entry = {
            "id": entry_id["id"],
            "question": entry_question["question"],
            "query": entry_query["query"],
            "answers": entry_answers["answers"],
        }

        return qald_entry

    def get_question_lang_and_strings(self, languages) -> list:
        question_lang_and_string = []
        for language in languages:
            if language in self.questions:
                question_string = self.questions[language].question_string
                question_lang_and_string.append(
                    {
                        "language": language,
                        "string": question_string
                    }
                )
        return question_lang_and_string
    

    def update_answer(self):
        self.answers = self.query.get_answer()