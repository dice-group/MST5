from components.Knowledge_graph import Knowledge_graph
from utils.data_io import *
from dataset.Dataset import Dataset, Entry
from components.Language import Language
from components.Question import Question
from components.Query import Query
from tqdm import tqdm
from sklearn.model_selection import train_test_split

class Qald(Dataset):
    
    
    def __init__(self, arg2, knowledge_graph=None, is_predicted=False) -> None:
        self.is_predicted = is_predicted
        if isinstance(arg2, dict):
            self.init1(arg2, knowledge_graph)
        if isinstance(arg2, list):
            self.init2(arg2, knowledge_graph)
    
    def init1(self, qald_file: dict={}, knowledge_graph=None) -> None:
        self.knowledge_graph = Knowledge_graph[knowledge_graph]
        self.entries = self.build_qald_list(qald_file)
    
    def init2(self, entries: list, knowledge_graph=None) -> None:
        self.knowledge_graph = Knowledge_graph[knowledge_graph]
        self.entries = entries

    def build_qald_list(self, qald_dataset: dict) -> list:
        qald_list = []
        if qald_dataset:
            dataset = qald_dataset["questions"]
            for entry in dataset:
                qald_entry = Qald_entry(entry["id"], entry["question"], entry["query"]["sparql"], self.knowledge_graph, entry["answers"], self.is_predicted)
                qald_list.append(qald_entry)
        return qald_list
    
    def add_entry(self, id, language, question_string, sparql, answers=None):
        question = [{
            "language": language,
            "string": question_string
        }]
        self.entries.append(Qald_entry(id, question, sparql, self.knowledge_graph, answers, self.is_predicted))


    def export_train_csv(
            self, 
            output_file, 
            languages, 
            include_linguistic_context=False, 
            include_entity_knowledge=False,
            question_padding_length=0,
            entity_padding_length=0,
            extend_with_noisy_entities=False,
            train_split_percent=100) -> None:
        # If train_split_percent is less than 100, then split the entries
        splits = []
        if train_split_percent < 100 :
            # split the files
            train, eval = train_test_split(self.entries, train_size= float(train_split_percent) / 100, random_state=42)
            splits.append((output_file + '_train_'+ str(train_split_percent) + 'pct.csv', train, extend_with_noisy_entities))
            splits.append((output_file + '_dev_'+ str(100 - int(train_split_percent)) +'pct.csv', eval, True))
        else:
            splits.append((output_file + '_full.csv', self.entries, extend_with_noisy_entities))
        
        for split in splits:
            csv_dataset = self.to_train_csv(
                split[1],
                languages,
                include_linguistic_context, 
                include_entity_knowledge,
                question_padding_length,
                entity_padding_length,
                split[2]
                )
            export_csv(split[0], csv_dataset)

    def to_train_csv(
            self,
            entries, 
            languages, 
            include_linguistic_context, 
            include_entity_knowledge,
            question_padding_length,
            entity_padding_length,
            extend_with_noisy_entities=False):
        csv_dataset = [["question", "query"]]
        entry: Qald_entry
        print("Preparing QALD CSV")
        for entry in tqdm(entries):
            sparql = entry.query.preprocess()
            for language in languages:
                if language in entry.questions:
                    question: Question = entry.questions[language]
                    question_string = super().get_question_string(
                        entry, 
                        question, 
                        include_linguistic_context, 
                        include_entity_knowledge,
                        pred=False,
                        question_padding_length=question_padding_length,
                        entity_padding_length=entity_padding_length)
                    csv_dataset.append([question_string, sparql])
                    if extend_with_noisy_entities:
                        question_string = super().get_question_string(
                            entry, 
                            question, 
                            include_linguistic_context, 
                            include_entity_knowledge,
                            pred=True,
                            question_padding_length=question_padding_length,
                            entity_padding_length=entity_padding_length)
                        csv_dataset.append([question_string, sparql])
        return csv_dataset


    def export_qald_json(self, languages: list, output: str) -> None:
        qald_entries: list = []
        qald_entry: Qald_entry
        for qald_entry in self.entries:
            qald_entries.append(qald_entry.build_qald_format_entry(languages))
        export_json(output, {"questions": qald_entries})


    def get_id_question_list(
            self, 
            language, 
            include_linguistic_context: bool = False, 
            include_entity_knowledge: bool = False,
            question_padding_length = 0,
            entity_padding_length = 0,
            use_gold_ents = False,
            translate_target_lang = None) -> list:
        questions_with_id = []
        entry: Qald_entry
        print(f'Generating question strings for {language}')
        for entry in tqdm(self.entries):
            if language in entry.questions:
                question: Question = entry.questions[language]
                question_string = super().get_question_string(
                    entry, 
                    question, 
                    include_linguistic_context, 
                    include_entity_knowledge, 
                    pred=(not use_gold_ents),
                    question_padding_length=question_padding_length,
                    entity_padding_length=entity_padding_length,
                    translate_target_lang=translate_target_lang
                    )
                questions_with_id.append([entry.id, question_string])
        return questions_with_id
    

    def update_answers(self):
        qald_entry: Qald_entry
        for qald_entry in self.entries:
            qald_entry.update_answer()



class Qald_entry(Entry):
    
    def __init__(self, id, questions, sparql, knowledge_graph, answers=None, is_predicted=False) -> None:
        self.is_predicted = is_predicted
        self.query_exec_info = {}
        if isinstance(sparql, str):
            self.init1(id, questions, sparql, knowledge_graph, answers)
        if isinstance(sparql, Query):
            self.init2(id, questions, sparql, answers)
            
    
    def init1(self, id, questions, sparql, knowledge_graph, answers=None) -> None:
        self.id = id
        self.questions: dict[str, Question] = self.build_questions(questions)
        self.query: Query = super().build_query(sparql, knowledge_graph, self.is_predicted)
        self.answers = answers
        
    def init2(self, id, questions: dict[str, Question], query: Query, answers=[]) -> None:
        self.id = id
        self.questions = questions
        self.query = query
        self.answers = answers

    def build_questions(self, questions: list[dict]) -> dict:
        entry_questions = {}
        for q in questions:
            try:
                entry_questions[q["language"]] = Question(q["string"], Language[q["language"]])
            except:
                pass
        return entry_questions


    def get_entity_knowledge(self) -> list:
        return self.query.get_entity_knowledge()


    def build_qald_format_entry(self, languages: list) -> dict:
        question_lang_and_string = self.get_question_lang_and_strings(languages)
        return super().build_qald_format_entry(self.id, question_lang_and_string, self.query.sparql, self.answers)

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
        self.query_exec_info = self.query.get_answer()
        self.query_exec_info['id'] = self.id
        self.answers = self.query_exec_info['answer']