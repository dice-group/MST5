from components.Knowledge_graph import Knowledge_graph
from components.Query import Query
from components.Language import Language
import requests
import json

class Question:
    def __init__(self, question_string: str, language: Language) -> None:
        self.question_string = question_string
        self.language = language


    def get_question_string_with_lingtuistic_context(self):
        _, pos, dep, dep_depth = self.get_linguistic_context()
        padded_question_string = self.pad_to_64()
        padded_pos_tags = self.pad_to_64(" ".join(pos))
        padded_dependency_relations = self.pad_to_64(" ".join(dep))
        padded_dependency_depth = self.pad_to_64(" ".join(map(str, dep_depth)))
        return f"{padded_question_string} {padded_pos_tags} {padded_dependency_relations} {padded_dependency_depth}"
    
    def get_linguistic_context(self):
        nlp = Language.get_spacy_nlp(self.language)
        doc = self.get_doc(self.question_string, nlp)
        pos = self.get_pos_tags(doc)
        dep = self.get_dependency_relation(doc)
        root = self.get_root_node(doc, dep)
        depth_list = self.get_dependency_relation_depth(root, [-1] * len(doc))
        return doc, pos, dep, depth_list

    def get_doc(self, text, nlp):
        return nlp(text)

    def get_pos_tags(self, doc):
        return [token.pos_ for token in doc]

    def get_dependency_relation(self, doc):
        return [token.dep_ for token in doc]

    def get_root_node(self, doc, dep):
        return doc[dep.index("ROOT")]

    def get_dependency_relation_depth(self, root, depth_list, depth=1):
        depth_list[root.i] = depth
        if len(list(root.children)) == 0:
            return depth_list
        for child in root.children:
            depth_list = self.get_dependency_relation_depth(child, depth_list, depth + 1)
        return depth_list
    
    def pad_to_64(self, string: str=None):
        if not string:
            string = self.question_string
        tokens = string.split()
        padded_tokens = tokens[:64] + ["<pad>"] * max(0, 64 - len(tokens))
        padded_question = " ".join(padded_tokens)
        return padded_question


    def add_entity_knowledge(self, question_string, entity_knowledge):
        
        return question_string + " <pad> " + " ".join(entity_knowledge)
    

    def recognize_entities(self, ner, el):
        ner_response = self.send_entity_detection_request(ner, el)
        if el=="mgenre_el":
            entities = self.process_wikidata_ner_response(ner_response)
        elif el=="mag_el":
            entities = self.process_dbpedia_ner_response(ner_response)
        return list(entities.values())

    def send_entity_detection_request(self, ner, el):
        url = 'http://nebula.cs.upb.de:6100/custom-pipeline'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'query': self.question_string,
            'full_json': 'True',
            'components': f'{ner}, {el}',
            'lang': self.language.value
        }

        response = requests.post(url, headers=headers, data=data)
        return response.text
    
    def process_wikidata_ner_response(self, ner_response:str):
        entities = {}
        response: dict = self.convert_ner_response_to_dict(ner_response)
        detection: dict
        for detection in response["ent_mentions"]:
            try:
                link_candidates = detection["link_candidates"]
                entity_name, _, entity_id = link_candidates[0]
                entities[entity_name] = f"wd_{entity_id}"
            except:
                pass
        return entities
    
    def process_dbpedia_ner_response(self, ner_response: str):
        entities = {}
        response: dict = self.convert_ner_response_to_dict(ner_response)
        detection: dict
        if "ent_mentions" in response:
            for detection in response["ent_mentions"]:
                try:
                    uri = detection["link"]
                    uri = self.process_dbpedia_uri(uri)
                    entities[detection["surface_form"]] = uri
                except:
                    pass
        return entities
    
    def convert_ner_response_to_dict(self, ner_response) -> dict:
        ner_response = ner_response.replace("false", '''"False"''')
        ner_response = ner_response.replace("true", '''"True"''')
        return json.loads(ner_response)
    
    def process_dbpedia_uri(self, uri:str):
        if self.is_uri_not_in_en(uri):
            ask_sameAs_sparql = f"SELECT DISTINCT ?uri WHERE {{ ?uri owl:sameAs <{uri}> .}}"
            query = Query(ask_sameAs_sparql, Knowledge_graph.DBpedia)
            uri = query.get_en_uri()
        uri = uri.replace("http://dbpedia.org/resource/", "dbr_")
        return uri

    def is_uri_not_in_en(self, uri):
        return 'fr' in uri or 'de' in uri





