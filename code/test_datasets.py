import unittest
from dataset.LCquad1 import LCquad1Entry
from components.Language import Language
from components.Knowledge_graph import Knowledge_graph
from components.Query import Query

class LCquad1Test(unittest.TestCase):
    def test_parse_lcquad_entry(self):		
        input_entry = {
        "_id": "1501", 
        "corrected_question": "How many movies did Stanley Kubrick direct?", 
        "intermediary_question": "How many <movies> are there whose <director> is <Stanley Kubrick>?", 
        "sparql_query": "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", 
        "sparql_template_id": 101
        }
        entry = LCquad1Entry(input_entry)
        self.assertEqual(entry.question.question_string, "How many movies did Stanley Kubrick direct?")
        self.assertEqual(entry.question.language, Language.en)
        self.assertEqual(entry.query.sparql, "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }")
        self.assertEqual(entry.query.knowledge_graph, Knowledge_graph.DBpedia)

    
    def test_return_sparql_query(self):
        input_entry = {"_id": "1501", 
                "corrected_question": "How many movies did Stanley Kubrick direct?", 
                "intermediary_question": "How many <movies> are there whose <director> is <Stanley Kubrick>?", 
                "sparql_query": "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", 
                "sparql_template_id": 101}

        entry = LCquad1Entry(input_entry)
        query = entry.get_query_from_input_entry(input_entry)

        expected_query = Query("SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", Knowledge_graph.DBpedia)


        self.assertEqual(query.sparql, expected_query.sparql)
        self.assertEqual(query.knowledge_graph, expected_query.knowledge_graph)


if __name__ == '__main__':
	unittest.main()
