import unittest
from components.Language import Language
from components.Query import Query
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph


class Test_Language(unittest.TestCase):
    def test_get_nlp(self):
        Language.get_spacy_nlp(Language.en)

class Test_Question(unittest.TestCase):
    def setUp(self) -> None:
        self.question = Question("Ist Hawaii der Geburtsort von Trump?", Language.de)
        return super().setUp()

    def test_input_length(self):
        question_string = "What is the common affiliation of the Monroe Carell Jr. Children's Hospital at Vanderbilt and alma mater of the Duncan U. Fletcher? <pad> PRON AUX DET ADJ NOUN ADP DET PROPN PROPN PROPN PROPN PART PROPN ADP PROPN CCONJ NOUN NOUN ADP DET PROPN PROPN PROPN PUNCT <pad> attr ROOT det amod nsubj prep det compound compound compound poss case pobj prep pobj cc compound conj prep det compound compound pobj punct <pad> 2 1 3 3 2 3 6 7 7 6 5 6 4 5 6 7 6 5 6 8 8 8 7 2 <pad> dbr_Monroe_Carell_Jr dbr_Duncan_U"
        question_string_split = question_string.split(" ")
        # self.assertEqual(question_string_split, "?")
        self.assertLessEqual(len(question_string_split), 128)

    def test_recognize_entities(self):
        pass

    def test_detect_entity_with_davlan(self):
        self.question = Question("Ist Hawaii der Geburtsort von Trump?", Language.de)
        response = self.question.send_entity_detection_request("davlan_ner")
        self.assertTrue("ent_mentions" in response)
        print(response)

    def test_process_ner_response(self):
        response = '''{"components":"davlan_ner, mgenre_el","ent_mentions":[{"end":10,"link":"Q782","link_candidates":[["Hawaii","de","Q782"]],"start":4,"surface_form":"Hawaii"},{"end":35,"link":"Q22686","link_candidates":[["Donald Trump","de","Q22686"]],"start":30,"surface_form":"Trump"}],"kb":"wd","lang":"de","placeholder":"00","replace_before":false,"text":"Ist Hawaii der Geburtsort von Trump?"}'''
        entities = self.question.process_ner_response(response)
        self.assertEqual(entities["Hawaii"], "Q782")
        self.assertEqual(entities["Donald Trump"], "Q22686")
        

class Test_Query(unittest.TestCase):
    def setUp(self) -> None:
        self.query = Query("SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", Knowledge_graph.DBpedia)
        return super().setUp()
    
    def test_replace_prefix_abbr(self):
        processed_sparql = self.query.replace_prefix_abbr(self.query.sparql)
        self.assertFalse("http://dbpedia.org/ontology" in processed_sparql)
        self.assertFalse("http://dbpedia.org/resource/" in processed_sparql)

    def test_delete_sparql_prefix(self):
        query = Query("PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { ?uri wdt:P31 wd:Q8502 ; wdt:P2044 ?elevation ; wdt:P17 wd:Q183 . } ORDER BY DESC(?elevation) LIMIT 1", Knowledge_graph.Wikidata)
        processed_sparql = query.delete_sparql_prefix(self.query.sparql)
        self.assertFalse("PREFIX" in processed_sparql)
        self.assertFalse("http://www.wikidata.org/entity/" in processed_sparql)

    
    def test_preprocess_sparql(self):
        preprocessed_query = self.query.preprocess()
        self.assertTrue(not ":" in preprocessed_query)

    def test_get_entities(self):
        entities = self.query.get_entity_knowledge()
        self.assertTrue("dbr_" in entities[0])

    def test_get_dbpedia_answer(self):
        answer = self.query.get_answer()
        self.assertTrue(answer["results"]["bindings"])

    def test_get_wikidata_answer(self):
        wikidata_query = Query("SELECT DISTINCT ?o1 WHERE { <http://www.wikidata.org/entity/Q23337>  <http://www.wikidata.org/prop/direct/P421>  ?o1 .  }", Knowledge_graph.Wikidata)
        answer = wikidata_query.get_answer()
        self.assertTrue(answer["results"]["bindings"])


if __name__ == '__main__':
    unittest.main()
