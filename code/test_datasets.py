import unittest
from dataset.LCquad1 import LCquad1, LCquad1Entry
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

class Test_LCquad1(unittest.TestCase):
     def setUp(self) -> None:
        self.entries = [
        {
                "_id": "1501", 
                "corrected_question": "How many movies did Stanley Kubrick direct?", 
                "intermediary_question": "How many <movies> are there whose <director> is <Stanley Kubrick>?", 
                "sparql_query": "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", 
                "sparql_template_id": 101
        }, 
        {
                "_id": "2586", 
                "corrected_question": "Which city's foundeer is John Forbes?", 
                "intermediary_question": "What <city>'s <founded by> is <John Forbes (British Army officer)>", 
                "sparql_query": "SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/ontology/founder> <http://dbpedia.org/resource/John_Forbes_(British_Army_officer)>  . ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/City>}", 
                "sparql_template_id": 301
        }, 
        {
                "_id": "2653", 
                "corrected_question": "What is the river whose mouth is in deadsea?", 
                "intermediary_question": "What is the <river> whose <river mouth> is <Dead Sea>?", 
                "sparql_query": "SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/ontology/riverMouth> <http://dbpedia.org/resource/Dead_Sea>  . ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/River>}", 
                "sparql_template_id": 301
        } ]
        self.lcquad = LCquad1(self.entries)
          
     def test_lcquad_entries(self):
        second_question_string = self.lcquad.entries[1].question.question_string
        self.assertEqual(second_question_string, "Which city's foundeer is John Forbes?")

     def test_get_csv_format(self):
        csv = self.lcquad.to_train_csv()
        header = csv[0]
        first_question, _ = csv[1]
        self.assertEqual(header, ['question', 'query'])
        self.assertEqual(first_question, "How many movies did Stanley Kubrick direct?")




if __name__ == '__main__':
	unittest.main()
