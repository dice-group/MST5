import unittest
from components.Language import Language
from components.Query import Query
from components.Question import Question
from components.Knowledge_graph import Knowledge_graph


class Test_Language(unittest.TestCase):
    def test_get_nlp(self):
        Language.get_spacy_nlp(Language.en)

    def test_get_supported_ner_for_en(self):
        ner = Language.get_supported_ner(Language.en)
        self.assertEqual(ner, "flair_ner")

    def test_get_babelspace_ner_for_zh(self):
        ner = Language.get_supported_ner(Language.zh)
        self.assertEqual(ner, "davlan_ner")

    def test_no_ner_for_ja(self):
        ner = Language.get_supported_ner(Language.ja)
        self.assertEqual(ner, "no_ner")


class Test_Question(unittest.TestCase):
    def setUp(self) -> None:
        self.question = Question("Ist Hawaii der Geburtsort von Trump?", Language.de)
        return super().setUp()

    def test_input_length(self):
        question_string = "What is the common affiliation of the Monroe Carell Jr. Children's Hospital at Vanderbilt and alma mater of the Duncan U. Fletcher? <pad> PRON AUX DET ADJ NOUN ADP DET PROPN PROPN PROPN PROPN PART PROPN ADP PROPN CCONJ NOUN NOUN ADP DET PROPN PROPN PROPN PUNCT <pad> attr ROOT det amod nsubj prep det compound compound compound poss case pobj prep pobj cc compound conj prep det compound compound pobj punct <pad> 2 1 3 3 2 3 6 7 7 6 5 6 4 5 6 7 6 5 6 8 8 8 7 2 <pad> dbr_Monroe_Carell_Jr dbr_Duncan_U"
        question_string_split = question_string.split(" ")
        self.assertLessEqual(len(question_string_split), 128)

    def test_detect_entity_with_flair_and_mgenre_el_for_wikidata(self):
        response = self.question.send_entity_detection_request("flair_ner", "mgenre_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("Trump" in response)

    def test_detect_entity_with_davlan_mgenre_el_for_wikidata(self):
        response = self.question.send_entity_detection_request("davlan_ner", "mgenre_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("Trump" in response)


    def test_detect_entity_with_mag_el_for_dbpedia_en(self):
        question = Question("Who wrote Harry Potter?", Language.en)
        response = question.send_entity_detection_request("babelscape_ner","mag_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("http://dbpedia.org/resource" in response)

    def test_detect_entity_with_mag_el_for_dbpedia_de(self):
        question = Question("Welcher US-Bundesstaat hat die höchste Bevölkerungsdichte?", Language.de)
        response = question.send_entity_detection_request("babelscape_ner","mag_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("http://de.dbpedia.org/resource" in response)

    def test_detect_entity_with_mag_el_for_dbpedia_de2(self):
        question = Question("Which German cities have more than 250000 inhabitants?", Language.de)
        response = question.send_entity_detection_request("babelscape_ner","mag_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("http://de.dbpedia.org/resource" in response)
    
    def test_detect_entity_with_mag_el_for_dbpedia_fr(self):
        question = Question("Qui a écrit Harry Potter?", Language.fr)
        response = question.send_entity_detection_request("babelscape_ner","mag_el")
        self.assertTrue("ent_mentions" in response)
        self.assertTrue("http://fr.dbpedia.org/resource" in response)

    def test_detect_entity_with_flair_and_mag_for_dbpedia(self):
        question = Question("Who wrote Harry Potter?", Language.en)
        response = question.send_entity_detection_request("flair_ner","mag_el")
        self.assertTrue("ent_mentions" in response)
        '''
        {"components":"flair_ner, mag_el","ent_mentions":[{"end":22,"link":"http://dbpedia.org/resource/IGN","start":10,"surface_form":"Harry Potter"}],"kb":"dbp","lang":"en","placeholder":"00","replace_before":false,"text":"Who wrote Harry Potter?"}
        '''
    

    def test_process_wikidata_ner_response(self):
        response = '''{"components":"davlan_ner, mgenre_el","ent_mentions":[{"end":10,"link":"Q782","link_candidates":[["Hawaii","de","Q782"]],"start":4,"surface_form":"Hawaii"},{"end":35,"link":"Q22686","link_candidates":[["Donald Trump","de","Q22686"]],"start":30,"surface_form":"Trump"}],"kb":"wd","lang":"de","placeholder":"00","replace_before":false,"text":"Ist Hawaii der Geburtsort von Trump?"}'''
        entities = self.question.process_wikidata_ner_response(response)
        self.assertEqual(entities["Hawaii"], "wd_Q782")
        self.assertEqual(entities["Donald Trump"], "wd_Q22686")

    def test_process_dbpedia_ner_response(self):
        response = '''{"components":"babelscape_ner, mag_el","ent_mentions":[{"end":22,"link":"http://dbpedia.org/resource/IGN","start":10,"surface_form":"Harry Potter"}],"kb":"dbp","lang":"en","placeholder":"00","replace_before":false,"text":"Who wrote Harry Potter?"}'''
        entities = self.question.process_dbpedia_ner_response(response)
        self.assertEqual(entities["Harry Potter"], "dbr_IGN")


    def test_process_dbpedia_ner_response_fr(self):
        response = '''{"components":"babelscape_ner, mag_el","ent_mentions":[{"end":24,"link":"http://fr.dbpedia.org/resource/Harry_Potter","start":12,"surface_form":"Harry Potter"}],"kb":"dbp","lang":"fr","placeholder":"00","replace_before":false,"text":"Qui a \u00e9crit Harry Potter?"}'''
        entities = self.question.process_dbpedia_ner_response(response)
        self.assertEqual(entities["Harry Potter"], "dbr_Harry_Potter")

    def test_process_dbpedia_uri(self):
        uri = "http://fr.dbpedia.org/resource/Harry_Potter"
        en_uri = self.question.process_dbpedia_uri(uri)
        self.assertEqual(en_uri, "dbr_Harry_Potter")

    def test_pad_question_string(self):
        question_string: str = self.question.pad_to_length()
        self.assertTrue("<pad>" in question_string)
        self.assertTrue(len(question_string.split(" ")), 64)

    def test_pad_pos(self):
        pos_tags = "PRON AUX DET ADJ NOUN ADP NOUN ADP PROPN PROPN PROPN"
        padded_pos_tags = self.question.pad_to_length(pos_tags, 64)
        self.assertTrue("<pad>" in padded_pos_tags)
        self.assertTrue(len(padded_pos_tags.split(" ")), 64)

    def test_length_after_padding(self):
        question_string_with_lc = self.question.get_question_string_with_lingtuistic_context()
        self.assertEqual(len(question_string_with_lc.split(" ")), 256)
        self.assertTrue("ROOT" in question_string_with_lc)


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

    def test_get_sameAs_uri(self):
        ask_sameAs_sparql = "SELECT DISTINCT ?uri WHERE { ?uri owl:sameAs <http://fr.dbpedia.org/resource/Donald_Trump> .}"
        query = Query(ask_sameAs_sparql, Knowledge_graph.DBpedia)
        en_uri = query.get_en_uri()
        self.assertEqual("http://dbpedia.org/resource/Donald_Trump", en_uri)



if __name__ == '__main__':
    unittest.main()
