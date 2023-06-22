from utils.data_io import *
from utils.query import preprocess_sparql, ask_wikidata
from utils.linguistic_parser import get_linguistic_context
import spacy
import re

nlp_en = spacy.load("en_core_web_sm")
nlp_zh = spacy.load("zh_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")
nlp_ja = spacy.load("ja_core_news_sm")
nlp_lt = spacy.load("lt_core_news_sm")
nlp_ru = spacy.load("ru_core_news_sm")
nlp_uk = spacy.load("uk_core_news_sm")

nlp_dict = {
    "en": nlp_en,
    "zh": nlp_zh,
    "de": nlp_de,
    "fr": nlp_fr,
    "ja": nlp_ja,
    "lt": nlp_lt,
    "uk": nlp_uk,
    "ru": nlp_ru,
    "ba": nlp_ru,
    "be": nlp_ru
}


class Qald:
    def __init__(self, qald_file: dict) -> None:
        self.qald = self.init_qald_list(qald_file)

    def init_qald_list(self, qald_dataset: dict) -> list:
        qald_list = []
        if qald_dataset:
            dataset = qald_dataset["questions"]
            for entry in dataset:
                qald_entry = Qald_entry(entry["id"], entry["question"], entry["query"]["sparql"], entry["answers"])
                qald_list.append(qald_entry)
        return qald_list
    
    def add_entry(self, id, language, question_string, query, answers):
        question = [{
            "language": language,
            "string": question_string
        }]
        self.qald.append(Qald_entry(id, question, query, answers))

    def export_train_csv(self, output_file, languages, include_linguistic_context=False, include_entity_knowledge=False) -> None:
        csv_dataset = [["question", "query"]]
        qald_entry: Qald_entry
        for qald_entry in self.qald:
            query = qald_entry.preprocessed_query
            for language in languages:
                if language in qald_entry.questions:
                    question = qald_entry.get_question_string_by_language(language, include_linguistic_context, include_entity_knowledge)
                    csv_dataset.append([question, query])
        export_csv(output_file, csv_dataset)
    

    def export_qald_json(self, languages: list, output: str, include_linguistic_context: bool = False, include_entity_knowledge: bool = False) -> None:
        qald_entries: list = []
        qald_entry: Qald_entry
        for qald_entry in self.qald:
            qald_entries.append(qald_entry.build_qald_format_entry(
                languages, include_linguistic_context, include_entity_knowledge))
        export_json(output, {"questions": qald_entries})

    def get_question_string_with_id(self, language, include_linguistic_context: bool = False, include_entity_knowledge: bool = False) -> list:
        questions_with_id = []
        qald_entry: Qald_entry
        for qald_entry in self.qald:
            if language in qald_entry.questions:
                question_string = qald_entry.get_question_string_by_language(language, include_linguistic_context, include_entity_knowledge)
                questions_with_id.append([qald_entry.id, question_string])
        return questions_with_id
    
    def update_answers(self):
        qald_entry: Qald_entry
        for qald_entry in self.qald:
            qald_entry.update_answer()

class Qald_entry:
    def __init__(self, id, questions, query, answers) -> None:
        self.id = id
        self.questions: dict = self.get_questions(questions)
        self.query = query
        self.preprocessed_query = preprocess_sparql(query)
        self.answers = answers

    def get_questions(self, questions: list) -> dict:
        question_strings = {}
        for q in questions:
            language = q["language"]
            question_strings[language] = Question(language, q["string"])
        return question_strings

    def get_entity_knowledge(self) -> list:
        pattern = r'\bwd_\w+\b'
        entities = re.findall(pattern, self.preprocessed_query)
        return entities


    def build_qald_format_entry(self, languages: list, include_linguistic_context: bool, include_entity_knowledge: bool) -> dict:
        entry_id = {"id": self.id}

        question_lang_and_string = self.get_question_lang_and_strings(
            languages, include_linguistic_context, include_entity_knowledge)

        entry_question = {
            "question": question_lang_and_string
        }

        entry_query = {"query": {"sparql": self.query}}

        entry_answers: dict = {"answers": [self.answers]}

        qald_entry = {
            "id": entry_id["id"],
            "question": entry_question["question"],
            "query": entry_query["query"],
            "answers": entry_answers["answers"],
        }

        return qald_entry

    def get_question_lang_and_strings(self, languages, include_linguistic_context: bool, include_entity_knowledge: bool) -> list:
        question_lang_and_string = []
        entity_knowledge = []
        if include_entity_knowledge:
            entity_knowledge = self.get_entity_knowledge()
        for language in languages:
            if language in self.questions:
                question_string = self.questions[language].build_question_string(include_linguistic_context, entity_knowledge)
                question_lang_and_string.append(
                    {
                        "language": language,
                        "string": question_string
                    }
                )
        return question_lang_and_string
    
    def get_question_string_by_language(self, language, include_linguistic_context: bool, include_entity_knowledge: bool) -> str:
        entity_knowledge = []
        if include_entity_knowledge:
            entity_knowledge = self.get_entity_knowledge()
        return self.questions[language].build_question_string(include_linguistic_context, entity_knowledge)

    def update_answer(self):
        self.answers = ask_wikidata(self.query)
        print(self.query)
        print(self.answers)


class Question:
    def __init__(self, language, question_string) -> None:
        self.language = language
        self.string = question_string

    def add_linguistic_context(self, nlp):
        self.doc, self.pos, self.dep, self.dep_depth = get_linguistic_context(
            nlp, self.string)

    def add_entity_knowledge(self, entities):
        self.entities = entities

    def build_question_string(self, include_linguistic_context: bool, entity_knowledge: list):
        question_string = self.string
        if include_linguistic_context:
            self.add_linguistic_context(nlp_dict[self.language])
            question_string += " <pad> " + " ".join(self.pos) \
                + " <pad> " + " ".join(self.dep) \
                + " <pad> " + " ".join(map(str, self.dep_depth))
        if entity_knowledge:
            question_string += " <pad> " + " ".join(entity_knowledge)
        return question_string
