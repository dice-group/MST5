import unittest
from dataset.LCquad1 import LCquad1, LCquad1_entry
from dataset.LCquad2 import LCquad2, LCquad2_entry
from dataset.Qald import Qald, Qald_entry
from components.Language import Language
from components.Knowledge_graph import Knowledge_graph
from components.Query import Query
from components.Question import Question


class Test_LCquad1_entry(unittest.TestCase):
    def setUp(self) -> None:
        self.input_entry = {"_id": "1501",
                            "corrected_question": "How many movies did Stanley Kubrick direct?",
                            "intermediary_question": "How many <movies> are there whose <director> is <Stanley Kubrick>?",
                            "sparql_query": "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }",
                            "sparql_template_id": 101}

        self.entry = LCquad1_entry(self.input_entry)

    def test_parse_lcquad_entry(self):
        self.assertEqual(self.entry.question.question_string,
                         "How many movies did Stanley Kubrick direct?")
        self.assertEqual(self.entry.question.language, Language.en)
        self.assertEqual(self.entry.query.sparql,
                         "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }")
        self.assertEqual(self.entry.query.knowledge_graph,
                         Knowledge_graph.DBpedia)

    def test_return_sparql_query(self):
        query: Query = self.entry.build_query_from_input_entry(self.input_entry)

        expected_query = Query(
            "SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/ontology/director> <http://dbpedia.org/resource/Stanley_Kubrick>  . }", Knowledge_graph.DBpedia)

        self.assertEqual(query.sparql, expected_query.sparql)
        self.assertEqual(query.knowledge_graph, expected_query.knowledge_graph)

    def test_return_question(self):

        question: Question = self.entry.build_question_from_input_query(
            self.input_entry)

        expected_question = Question(
            "How many movies did Stanley Kubrick direct?", Language.en)
        self.assertEqual(question.question_string,
                         expected_question.question_string)
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
            }]
        self.lcquad = LCquad1(self.entries)

    def test_lcquad_entries(self):
        second_question_string = self.lcquad.entries[1].question.question_string
        self.assertEqual(second_question_string,
                         "Which city's foundeer is John Forbes?")

    def test_get_csv_format(self):
        csv = self.lcquad.to_train_csv()
        header = csv[0]
        first_question, _ = csv[1]
        self.assertEqual(header, ['question', 'query'])
        self.assertEqual(
            first_question, "How many movies did Stanley Kubrick direct?")


class Test_Qald_entry(unittest.TestCase):
    def setUp(self) -> None:
        self.qald_id = "99"
        self.questions = [
            {
                "language": "en",
                "string": "What is the time zone of Salt Lake City?"
            },
            {
                "language": "de",
                "string": "Was ist die Zeitzone von Salt Lake City?"
            },
            {
                "language": "zh",
                "string": "盐湖城时区是什么？"
            },
            {
                "language": "ja",
                "string": "ソルトレイクシティのタイムゾーンは?"
            },
            {
                "language": "ru",
                "string": "В каком часовом поясе расположен Солт-Лейк-Сити?"
            },
            {
                "language": "uk",
                "string": "Який часовий пояс у Солт-Лейк Сіті?"
            },
            {
                "language": "ba",
                "string": "Ниндей вакыт поясы Солт-Лейк-Ситила"
            },
            {
                "language": "be",
                "string": "Які гадзінны пояс у Солт-Лэйк-Сіці"
            },
            {
                "language": "lt",
                "string": "Kokia laiko juosta yra Solt Leik Sityjes"
            }
        ]
        self.sparql = "SELECT DISTINCT ?o1 WHERE { <http://www.wikidata.org/entity/Q23337>  <http://www.wikidata.org/prop/direct/P421>  ?o1 .  }"
        self.answers = [
            {
                "head": {
                    "vars": [
                        "o1"
                    ]
                },
                "results": {
                    "bindings": [
                        {
                            "o1": {
                                "type": "uri",
                                "value": "http://www.wikidata.org/entity/Q3134980"
                            }
                        },
                        {
                            "o1": {
                                "type": "uri",
                                "value": "http://www.wikidata.org/entity/Q2212"
                            }
                        }
                    ]
                }
            }
        ]
        self.qald_entry = Qald_entry(
            self.qald_id, self.questions, self.sparql, Knowledge_graph.Wikidata, self.answers)
        return super().setUp()

    def test_build_questions(self):
        questions = self.qald_entry.build_questions(self.questions)

        self.assertEqual(questions["en"].question_string,
                         "What is the time zone of Salt Lake City?")
        self.assertEqual(questions["zh"].question_string, "盐湖城时区是什么？")

    def test_build_query(self):
        query = self.qald_entry.build_query(
            self.sparql, Knowledge_graph.Wikidata)

        self.assertEqual(query.sparql, self.sparql)
        self.assertEqual(query.knowledge_graph, Knowledge_graph.Wikidata)

    def test_get_dbpedia_entity_knowledge(self):
        qald_entry = Qald_entry(
            self.qald_id,
            self.questions,
            "PREFIX res: <http://dbpedia.org/resource/> PREFIX dbp: <http://dbpedia.org/property/> SELECT DISTINCT ?uri WHERE { res:Salt_Lake_City <http://dbpedia.org/ontology/timeZone> ?uri }",
            Knowledge_graph.DBpedia
        )

        entity_knowledge = qald_entry.get_entity_knowledge()
        self.assertTrue("res_" in entity_knowledge[0])

    def test_get_question_lang_and_strings(self):
        question_lang_and_strings = self.qald_entry.get_question_lang_and_strings([
                                                                                  "en", "de"])

        self.assertEqual(question_lang_and_strings[0]["language"], "en")
        self.assertEqual(
            question_lang_and_strings[0]["string"], "What is the time zone of Salt Lake City?")
        self.assertEqual(question_lang_and_strings[1]["language"], "de")
        self.assertEqual(
            question_lang_and_strings[1]["string"], "Was ist die Zeitzone von Salt Lake City?")

    def test_build_qald_format_entry(self):
        qald_format_entry = self.qald_entry.build_qald_format_entry([
                                                                    "en", "de"])

        self.assertEqual(qald_format_entry["id"], self.qald_id)
        self.assertEqual(qald_format_entry["query"]["sparql"], self.sparql)

    def test_update_answer(self):
        entry = Qald_entry(
            self.qald_id,
            self.questions,
            self.sparql,
            Knowledge_graph.Wikidata,
        )
        entry.update_answer()
        self.assertTrue(entry.answers["results"]["bindings"])

    def test_init_qald_entry(self):
        self.assertEqual(self.qald_entry.id, self.qald_id)
        self.assertEqual(
            self.qald_entry.questions["en"].question_string, "What is the time zone of Salt Lake City?")
        self.assertEqual(self.qald_entry.query.sparql, self.sparql)


class Test_Qald(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_qald = {
            "questions": [
                {
                    "id": "99",
                    "question": [
                        {
                            "language": "en",
                            "string": "What is the time zone of Salt Lake City?"
                        },
                        {
                            "language": "de",
                            "string": "In welcher Zeitzone liegt Salt Lake City?"
                        },
                        {
                            "language": "de",
                            "string": "Was ist die Zeitzone von Salt Lake City?"
                        },
                        {
                            "language": "ru",
                            "string": "Какой часовой пояс в Солт-Лейк-Сити"
                        },
                        {
                            "language": "ru",
                            "string": "В каком часовом поясе расположен Солт-Лейк-Сити?"
                        },
                        {
                            "language": "uk",
                            "string": "Який часовий пояс у Солт-Лейк Сіті?"
                        },
                        {
                            "language": "lt",
                            "string": "Kokia Solt Leik Sičio laiko zona?"
                        },
                        {
                            "language": "be",
                            "string": "Які гадзінны пояс у Солт-Лэйк-Сіці"
                        },
                        {
                            "language": "lt",
                            "string": "Kokia laiko juosta yra Solt Leik Sityjes"
                        },
                        {
                            "language": "ba",
                            "string": "Ниндей вакыт поясы Солт-Лейк-Ситила"
                        }
                    ],
                    "query": {
                        "sparql": "SELECT DISTINCT ?o1 WHERE { <http://www.wikidata.org/entity/Q23337>  <http://www.wikidata.org/prop/direct/P421>  ?o1 .  }"
                    },
                    "answers": [
                        {
                            "head": {
                                "vars": [
                                    "o1"
                                ]
                            },
                            "results": {
                                "bindings": [
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q3134980"
                                        }
                                    },
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q2212"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                {
                    "id": "98",
                    "question": [
                        {
                            "language": "en",
                            "string": "Who killed Caesar?"
                        },
                        {
                            "language": "de",
                            "string": "Wer hat Caesar ermordet?"
                        },
                        {
                            "language": "de",
                            "string": "Wer hat Cäsar getötet?"
                        },
                        {
                            "language": "ru",
                            "string": "Кто убил Цезаря"
                        },
                        {
                            "language": "uk",
                            "string": "Хто вбив Цезаря?"
                        },
                        {
                            "language": "lt",
                            "string": "Kas nužudė Cezarį?"
                        },
                        {
                            "language": "be",
                            "string": "Хто забіў Цэзара"
                        },
                        {
                            "language": "ba",
                            "string": "Кем Цезарьзы ултергэн?"
                        }
                    ],
                    "query": {
                        "sparql": "SELECT DISTINCT ?o1 WHERE { <http://www.wikidata.org/entity/Q1048>  <http://www.wikidata.org/prop/direct/P157>  ?o1 .  }"
                    },
                    "answers": [
                        {
                            "head": {
                                "vars": [
                                    "o1"
                                ]
                            },
                            "results": {
                                "bindings": [
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q172248"
                                        }
                                    },
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q207370"
                                        }
                                    },
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q294846"
                                        }
                                    },
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q1228715"
                                        }
                                    },
                                    {
                                        "o1": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q1243545"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                {
                    "id": "86",
                    "question": [
                        {
                            "language": "en",
                            "string": "What is the highest mountain in Germany?"
                        },
                        {
                            "language": "de",
                            "string": "Wie heißt der höchste Berg in Deutschland?"
                        },
                        {
                            "language": "ru",
                            "string": "Самая высокая гора в Германии?"
                        },
                        {
                            "language": "ru",
                            "string": "Самая высокая гора Германии?"
                        },
                        {
                            "language": "ru",
                            "string": "Какая гора самая высокая в Германии?"
                        },
                        {
                            "language": "ru",
                            "string": "Какая гора является самой высокой в Германии?"
                        },
                        {
                            "language": "uk",
                            "string": "Найвища гора в Німеччині?"
                        },
                        {
                            "language": "uk",
                            "string": "Яка найвища гора у Німеччині?"
                        },
                        {
                            "language": "be",
                            "string": "Самая высокая гара ў Германіі?"
                        },
                        {
                            "language": "lt",
                            "string": "Pats Aukščiausias kalnas Vokietijoje?"
                        },
                        {
                            "language": "lt",
                            "string": "Aukščiausias kalnas Vokietijoje?"
                        },
                        {
                            "language": "ba",
                            "string": "Германияла иң бейек тау?"
                        }
                    ],
                    "query": {
                        "sparql": "PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> SELECT ?uri WHERE { ?uri wdt:P31 wd:Q8502 ; wdt:P2044 ?elevation ; wdt:P17 wd:Q183 . } ORDER BY DESC(?elevation) LIMIT 1"
                    },
                    "answers": [
                        {
                            "head": {
                                "vars": [
                                    "uri"
                                ]
                            },
                            "results": {
                                "bindings": [
                                    {
                                        "uri": {
                                            "type": "uri",
                                            "value": "http://www.wikidata.org/entity/Q3375"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        self.qald = Qald(self.sample_qald, Knowledge_graph.Wikidata)
        return super().setUp()

    def test_add_entry(self):
        empty_qald = Qald()
        empty_qald.add_entry(
            "1",
            "en",
            "What is the time zone of Salt Lake City?",
            "SELECT DISTINCT ?o1 WHERE { <http://www.wikidata.org/entity/Q23337>  <http://www.wikidata.org/prop/direct/P421>  ?o1 .  }",
            Knowledge_graph.DBpedia
        )

        self.assertTrue(empty_qald.entries)

    def test_build_qald_list(self):
        empty_qald = Qald()
        qald_list = empty_qald.build_qald_list(self.sample_qald, Knowledge_graph.Wikidata)
        
        self.assertEqual(qald_list[0].id, "99")
        self.assertEqual(qald_list[1].id, "98")

    def test_get_id_question_list(self):
        id_question = self.qald.get_id_question_list("ru")
        self.assertEqual(id_question[1], ["98", "Кто убил Цезаря"])

    def test_get_id_question_list_with_ling_and_entity(self):
        id_question = self.qald.get_id_question_list("ru", True, True)
        self.assertEqual(id_question[1][0], "98")
        self.assertTrue("ROOT" in id_question[1][1])
        self.assertTrue("wd_" in id_question[1][1])

    def test_to_train_csv(self):
        train_csv = self.qald.to_train_csv(["en", "de"], False, False)
        self.assertEqual(train_csv[0], ["question", "query"])
        self.assertEqual(train_csv[1][0], "What is the time zone of Salt Lake City?")
        self.assertFalse(":" in train_csv[1][1])

    def test_to_train_csv_with_ling_and_entity(self):
        train_csv = self.qald.to_train_csv(["en", "de"], True, True)
        self.assertEqual(train_csv[0], ["question", "query"])
        self.assertTrue("ROOT" in train_csv[1][0])
        self.assertTrue("wd_" in train_csv[1][1])
        self.assertFalse(":" in train_csv[1][1])

class Test_LCquad2_query(unittest.TestCase):
    def setUp(self) -> None:
        lcquad2_entry = {
            "NNQT_question": "What is the {country} for {head of state} of {Mahmoud Abbas}",
            "uid": 20258,
            "subgraph": "simple question left",
            "template_index": 604,
            "question": "Who is the  {country} for {head of state} of {Mahmoud Abbas}",
            "sparql_wikidata": " select distinct ?sbj where { ?sbj wdt:P35 wd:Q127998 . ?sbj wdt:P31 wd:Q6256 } ",
            "sparql_dbpedia18": "select distinct ?subj where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> ?subj . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P35> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://wikidata.dbpedia.org/resource/Q127998> . ?subj <http://www.wikidata.org/entity/P31> <http://wikidata.dbpedia.org/resource/Q6256> } ",
            "template": "<?S P O ; ?S InstanceOf Type>",
            "answer": [],
            "template_id": 2,
            "paraphrased_question": "What country is Mahmoud Abbas the head of state of?"
        }
        self.entry = LCquad2_entry(lcquad2_entry["NNQT_question"], lcquad2_entry["uid"], lcquad2_entry["sparql_wikidata"], Knowledge_graph.Wikidata)
        return super().setUp()
    
    def test_build_question(self):
        entry = LCquad2_entry("", "", "", Knowledge_graph.Wikidata)
        question = entry.build_question("What is the {country} for {head of state} of {Mahmoud Abbas}", "en")
        self.assertEqual(question.question_string, "What is the country for head of state of Mahmoud Abbas")

    def test_build_query(self):
        entry = LCquad2_entry("", "", "", Knowledge_graph.Wikidata)
        query:Query = entry.build_query(" select distinct ?sbj where { ?sbj wdt:P35 wd:Q127998 . ?sbj wdt:P31 wd:Q6256 } ", Knowledge_graph.Wikidata)
        self.assertTrue("wdt:P35" in query.sparql)
        self.assertEqual(Knowledge_graph.Wikidata, query.knowledge_graph)
        

if __name__ == '__main__':
    unittest.main()
