import unittest
from components.Language import Language
from components.Query import Query
from components.Knowledge_graph import Knowledge_graph


class Test_Language(unittest.TestCase):
    def test_get_nlp(self):
        Language.get_spacy_nlp(Language.en)

class Test_Question(unittest.TestCase):
    pass

class Test_Query(unittest.TestCase):
    def setUp(self) -> None:
        self.query = Query("SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", Knowledge_graph.DBpedia)
        return super().setUp()
    
    def test_preprocess_sparql(self):
        preprocessed_query = self.query.preprocess()
        self.assertTrue(not ":" in preprocessed_query)

    def test_get_entities(self):
        entities = self.query.get_entity_knowledge()
        self.assertTrue("dbr_" in entities[0])