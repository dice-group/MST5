from components.Language import Language
import requests

class Question:
    def __init__(self, question_string: str, language: Language) -> None:
        self.question_string = question_string
        self.language = language


    def get_question_string_with_lingtuistic_context(self):
        _, pos, dep, depth_list = self.get_linguistic_context()
        return self.question_string + " <pad> " + " ".join(pos) \
                    + " <pad> " + " ".join(dep) \
                    + " <pad> " + " ".join(map(str, depth_list))

    def get_linguistic_context(self):
        nlp = Language.get_spacy_nlp(self.language)
        doc = self.get_doc(self.question_string, nlp)
        pos = self.get_pos(doc)
        dep = self.get_dep(doc)
        root = self.get_root_node(doc, dep)
        depth_list = self.get_dep_depth(root, [-1] * len(doc))
        return doc, pos, dep, depth_list

    def get_doc(self, text, nlp):
        return nlp(text)

    def get_pos(self, doc):
        return [token.pos_ for token in doc]

    def get_dep(self, doc):
        return [token.dep_ for token in doc]

    def get_root_node(self, doc, dep):
        return doc[dep.index("ROOT")]

    def get_dep_depth(self, root, depth_list, depth=1):
        depth_list[root.i] = depth
        if len(list(root.children)) == 0:
            return depth_list
        for child in root.children:
            depth_list = self.get_dep_depth(child, depth_list, depth + 1)
        return depth_list


    def add_entity_knowledge(self, question_string, entity_knowledge):
        return question_string + " <pad> " + " ".join(entity_knowledge)
    
    def recognize_entities(self, knowledge_graph):
        pass

    def send_entity_detection_request(self, ner):
        url = 'http://nebula.cs.upb.de:6100/custom-pipeline'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'query': self.question_string,
            'full_json': 'True',
            'components': f'{ner}, mgenre_el',
            'lang': self.language.value
        }

        response = requests.post(url, headers=headers, data=data)
        return response.text



