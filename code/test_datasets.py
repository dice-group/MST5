import unittest
from dataset.LCquad1 import LCquad1Entry
from components.Language import Language
from components.Knowledge_graph import Knowledge_graph
from components.Query import Query
from components.Question import Question

class LCquad1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.input_entry = {"_id": "1501", 
                "corrected_question": "How many movies did Stanley Kubrick direct?", 
                "intermediary_question": "How many <movies> are there whose <director> is <Stanley Kubrick>?", 
                "sparql_query": "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", 
                "sparql_template_id": 101}

        self.entry = LCquad1Entry(self.input_entry)

    def test_parse_lcquad_entry(self):		
        self.assertEqual(self.entry.question.question_string, "How many movies did Stanley Kubrick direct?")
        self.assertEqual(self.entry.question.language, Language.en)
        self.assertEqual(self.entry.query.sparql, "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }")
        self.assertEqual(self.entry.query.knowledge_graph, Knowledge_graph.DBpedia)

    
    def test_return_sparql_query(self):
        query: Query = self.entry.get_query_from_input_entry(self.input_entry)

        expected_query = Query("SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", Knowledge_graph.DBpedia)


        self.assertEqual(query.sparql, expected_query.sparql)
        self.assertEqual(query.knowledge_graph, expected_query.knowledge_graph)

    def test_return_question(self):
        
        question: Question = self.entry.get_question_from_input_query(self.input_entry)
        
        expected_question = Question("How many movies did Stanley Kubrick direct?", Language.en)
        self.assertEqual(question.question_string, expected_question.question_string)
        self.assertEqual(question.language, expected_question.language)


if __name__ == '__main__':
	unittest.main()
