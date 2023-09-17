from utils.data_io import read_json
from dataset.Qald import Qald, Qald_entry
from dataset.LCquad2 import LCquad2
import json

def update_qald_dataset(input_file_path, output_file_path, languages, kg):
    test_file = read_json(input_file_path)
    test_qald = Qald(test_file, kg)
    test_qald.update_answers()
    test_qald.export_qald_json(languages, output_file_path)
    

def convert_lcquad2_to_qald(input_file_path, output_file_path):
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
    
