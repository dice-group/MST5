from utils.data_io import read_json
from dataset.Qald import Qald, Qald_entry
from dataset.LCquad2 import LCquad2
import json

def update_qald_dataset(input_file_path: str, output_file_path: str, languages: list, kg):
    test_file = read_json(input_file_path)
    test_qald = Qald(test_file, kg)
    test_qald.update_answers()
    test_qald.export_qald_json(languages, output_file_path)
    

def convert_lcquad2_to_qald(input_file_path: str, output_file_path: str):
    knowledge_graph = "Wikidata"
    lcquad_data = LCquad2(read_json(input_file_path))
    qald_entries = []
    # For each enty in lcquad2 create Qald_entry object with empty answer
    for lcquad_entry in lcquad_data.entries:
        id = lcquad_entry.uid
        question_obj = lcquad_entry.question
        question_dict = {'en': question_obj}
        query = lcquad_entry.query
        qald_entry = Qald_entry(id, question_dict, query, knowledge_graph, [])
        qald_entries.append(qald_entry)
    # Create QALD object using qald_entries
    qald_dataset = Qald(qald_entries, knowledge_graph)
    # update answers
    qald_dataset.update_answers()
    # export the file
    qald_dataset.export_qald_json(['en'], output_file_path)

    
def convert_mintaka_to_qald(input_file_path: str, output_file_path: str, languages: list):
    """This function is create a QALD format file from a Mintaka format dataset.
        It only exclusively extracts questions, it does not extract answers due to its limited use-case.

    Args:
        input_file_path (str): path to the input file containing Mintaka dataset
        output_file_path (str): path to store the output file at
        languages (list): list of languages for which to extract the question translations
    """    
    knowledge_graph = "Wikidata"
    # Read mintaka json file
    with open(input_file_path,'r') as fp:
        mintaka_data = json.load(fp)
    qald_entries = []
    # For each question,
    for mintaka_question in mintaka_data: 
        # extract: id
        id = mintaka_question['id']
        # extract: question text in all the required languages
        en_question = mintaka_question['question']
        question_list = []
        translations = mintaka_question['translations']
        if "en" in languages:
            question_list.append({"language": "en", "string": en_question})
        for lang in languages:
            trans_question = translations.get(lang)
            if trans_question:
                question_list.append({"language": lang, "string": trans_question})
        # create Qald_entry object
        qald_entry = Qald_entry(id, question_list, '', knowledge_graph, [])
        # save to list
        qald_entries.append(qald_entry)
    # initiate QALD dataset
    qald_dataset = Qald(qald_entries, knowledge_graph)
    # export to file
    qald_dataset.export_qald_json(languages, output_file_path)
    
     
    
