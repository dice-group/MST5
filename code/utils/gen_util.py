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
    """
    This function is create a QALD format file from a Mintaka format dataset.
    It only exclusively extracts questions, it does not extract answers due to its limited use-case.

    Args:
        input_file_path (str): path to the input file containing Mintaka dataset.
        output_file_path (str): path to store the output file at.
        languages (list): list of languages for which to extract the question translations.
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
    

def extract_mintaka_qald_results(input_file_path: str, output_file_path: str):
    """
    Function to extract the results from QALD formatted Mintaka file. 
    The results are extracted as per the KG results format: https://github.com/amazon-science/mintaka#evaluation.

    Args:
        input_file_path (str): path to the input file containing QALD formatted Mintaka file.
        output_file_path (str): path to store output file at.
    """
    knowledge_graph = "Wikidata"
    qald_mintaka_file = read_json(input_file_path)
    qald_mintaka_file = Qald(qald_mintaka_file, knowledge_graph)
    output_dict = {}
    for entry in qald_mintaka_file.entries:
        id = entry.id
        answers_dict = entry.answers[0]
        output_dict[id] = format_mintaka_sparql_results(answers_dict)
        
    with open(output_file_path, 'w') as outfile:
        json.dump(output_dict, outfile, indent=4, sort_keys=True)
        
        
    
def format_mintaka_sparql_results(json_response):
    # Extract SPARQL results in this format: https://github.com/amazon-science/mintaka#evaluation
    # Check if the JSON response contains a "boolean" field (ask query).
    if "boolean" in json_response:
        return json_response["boolean"]
    
    # Check if the JSON response contains a "results" field (select or count query). Also, only process response with only one variable.
    elif "results" in json_response and len(json_response["head"]["vars"]) == 1:
        var_name = json_response["head"]["vars"][0]
        bindings = json_response["results"]["bindings"]

        # If there are no results, return an empty list.
        if not bindings or (not bindings[0]):
            return None

        # Check the type of the first result to determine if it's a URI or literal.
        first_result = bindings[0][var_name]

        # Check if the first result is a URI (resource).
        if first_result["type"] == "uri":
            if len(bindings) == 1:
                return first_result["value"]
            uris = [result[var_name]["value"] for result in bindings]
            return uris
        
        elif first_result["type"] == "literal":
            datatype = first_result.get("datatype", "notype")
            if len(bindings) == 1:
                return format_mintaka_literal(first_result["value"], datatype)
            ret_val = ''
            for result in bindings:
                if not result:
                    continue
                try:
                    literal_value = result[var_name]["value"]
                except Exception as e:
                    print(result)
                    raise
                ret_val += str(literal_value) + ' '
            return ret_val.strip()

    # If the JSON response doesn't match any known format, return None.
    return None
    
def format_mintaka_literal(literal_value, datatype):
    if datatype == "http://www.w3.org/2001/XMLSchema#integer":
        return int(literal_value)
    elif datatype == "http://www.w3.org/2001/XMLSchema#decimal":
        return float(literal_value)
    return literal_value
     
    
