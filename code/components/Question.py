from components.Language import Language

class Question:
    def __init__(self, question_string: str, language: Language) -> None:
        self.question_string = question_string
        self.language = language


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
