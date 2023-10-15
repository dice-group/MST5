from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from components.Query import Query
from components.Question import Question
from utils.data_io import export_csv
from tqdm import tqdm
class Dataset:
    def __init__(self, entries: list[Query], knowledge_graph=None):
        self.entries = entries
        self.knowledge_graph = knowledge_graph

    def export_train_csv(
            self, 
            output_file, 
            include_linguistic_context=False, 
            include_entity_knowledge=False,
            question_padding_length=0,
            entity_padding_length=0,
            extend_with_noisy_entities=False):
        csv_dataset = self.to_train_csv(
            include_linguistic_context, 
            include_entity_knowledge,
            question_padding_length,
            entity_padding_length,
            extend_with_noisy_entities
            )
        export_csv(output_file, csv_dataset)

    def to_train_csv(
            self, 
            include_linguistic_context=False, 
            include_entity_knowledge=False,
            question_padding_length=0,
            entity_padding_length=0,
            extend_with_noisy_entities=False):
        csv = [['question', 'query']]
        entry: Entry
        print("Preparing training CSV")
        for entry in tqdm(self.entries):
            question = entry.question
            question_string = self.get_question_string(
                entry, 
                question, 
                include_linguistic_context, 
                include_entity_knowledge,
                question_padding_length=question_padding_length,
                entity_padding_length=entity_padding_length)
            sparql = entry.query.preprocess()
            csv.append([question_string, sparql])
            if extend_with_noisy_entities:
                question_string = self.get_question_string(
                    entry, 
                    question, 
                    include_linguistic_context, 
                    include_entity_knowledge,
                    question_padding_length=question_padding_length,
                    entity_padding_length=entity_padding_length,
                    pred=True)
                csv.append([question_string, sparql])
                
                
        return csv

    def get_question_string(
            self, 
            entry, 
            question: Question, 
            include_linguistic_context: bool, 
            include_entity_knowledge: bool, 
            pred=False,
            question_padding_length=0,
            entity_padding_length=0):
        # question_string = question.question_string
        question_string = question.pad_to_length(question.question_string, length=question_padding_length)
        if include_linguistic_context:
            question_string = question.get_question_string_with_lingtuistic_context(question_padding_length)
        if include_entity_knowledge:
            if pred:
                if self.is_kg_wikidata():
                    entity_knowledge = self.get_wikidata_entities(entry, question)
                elif self.is_kg_dbpedia():
                    entity_knowledge = self.get_dbpedia_entities(question)
            else:
                entity_knowledge = entry.query.get_entity_knowledge()

            question_string = question.add_entity_knowledge(question_string, entity_knowledge, entity_padding_length)
        return question_string

    def is_kg_wikidata(self):
        return self.knowledge_graph==Knowledge_graph.Wikidata

    def is_kg_dbpedia(self):
        return self.knowledge_graph==Knowledge_graph.DBpedia
    
    def get_wikidata_entities(self, entry, question):
        ner = Language.get_supported_ner(question.language)
        
        ### Uncomment one of the following two blocks based on your requirement
        
        #### English-only entity disambiguation block start ###
        # entity_knowledge = entry.questions["en"].recognize_entities("flair_ner", "mgenre_el") # Extract entities using only the English text.
        #### English-only entity disambiguation block end ###
        
        #### Multilingual entity disambiguation block start ###
        if self.no_supported_ner(ner):
            entity_knowledge = question.recognize_entities("spacy_ner", "mgenre_el")
        else:
            entity_knowledge = question.recognize_entities(ner, "mgenre_el")
        #### Multilingual entity disambiguation block end ###
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
