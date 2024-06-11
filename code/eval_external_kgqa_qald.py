import argparse
from utils.data_io import read_json
from dataset.Qald import Qald
from tqdm import tqdm
import time
import os
from components.Gerbil import Gerbil
import requests
import traceback
from components.Knowledge_graph import Knowledge_graph

# Sample Usage: python code/eval_external_kgqa_qald.py --systems deeppavlov2023 --test datasets/qald10/qald_10.json --knowledge_graph Wikidata --languages en,ru --gerbil_eval --output_path predictions_external_qald10_test

# Host for https://github.com/WSE-research/qa-systems-wrapper
QASW_HOST = "http://141.57.8.18:40199/"

SYSTEM_DICT = {
    'qanswer': {'label': 'QAnswer', 'langs': ['en', 'ru', 'de', 'fr'], 'api_postfix': 'qanswer/answer', 'sparql_key': 'SPARQL', 'host': QASW_HOST, 'kg': Knowledge_graph.Wikidata},
    'deeppavlov2023': {'label': 'DeepPavlov 2023', 'langs': ['en', 'ru'], 'api_postfix': 'deeppavlov2023/answer_raw', 'sparql_key': 'sparql_query', 'host': QASW_HOST, 'kg': Knowledge_graph.Wikidata},
    'platypus': {'label': 'Platypus', 'langs': ['en', 'fr'], 'api_postfix': 'platypus/answer_raw', 'sparql_key': 'platypus:sparql', 'host': QASW_HOST, 'kg': Knowledge_graph.Wikidata},
    'tebaqa': {'label': 'TeBaQA', 'langs': ['en'], 'api_postfix': 'tebaqa/answer', 'sparql_key': 'sparql', 'host': QASW_HOST, 'kg': Knowledge_graph.DBpedia},
    'ganswer': {'label': 'gAnswer', 'langs': ['en'], 'api_postfix': 'gAnswer/query_candidates', 'sparql_key': 'queries', 'host': QASW_HOST, 'kg': Knowledge_graph.DBpedia},
    'qanary': {'label': 'qanary', 'langs': ['en'], 'api_postfix': 'qanary/query_candidates', 'sparql_key': 'queries', 'host': QASW_HOST, 'kg': Knowledge_graph.Wikidata}
}

def find_keys_nested(obj, key, collected_values=None):
    """Recursively search for values of a key in a nested dictionary or list."""
    if collected_values is None:
        collected_values = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                if isinstance(v, list):
                    collected_values.extend(v)
                else:
                    collected_values.append(v)
            if isinstance(v, (dict, list)):
                find_keys_nested(v, key, collected_values)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                find_keys_nested(item, key, collected_values)

    return collected_values

def extract_sparql(question, lang, system_id):
    print('Query:', question)
    system_info = SYSTEM_DICT[system_id]
    payload = {
        'question': question,
        'lang': lang
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    host = system_info['host']
    response = requests.request("GET", host + system_info['api_postfix'], headers=headers, params=payload, timeout=600)
    # print('Response received:', response)
    sparql_list = None
    if response.status_code == 200:
        response_json = response.json()
        # print('Response received:', response_json)
        sparql_keylink = system_info['sparql_key']
        sparql_list = find_keys_nested(response_json, sparql_keylink)
        print('SPARQLs extracted:', sparql_list)
        # sleep to avoid spam
        time.sleep(2)
    # extracted SPARQL
    return sparql_list[0] if sparql_list and isinstance(sparql_list[0], str) else ''


def main():
    parser = argparse.ArgumentParser(
        description="A program to use trained model to predict query, build qald dataset and evaluate predictions.")

    parser.add_argument("--systems", type=str,
                        help="commma separated (without spaces) ids of the external systems to evaluate", required=True)
    parser.add_argument("-t", "--test", type=str,
                        help="Name of test file.", required=True)
    parser.add_argument("--knowledge_graph", type=str,
                        help="Type of knowledge_graph.", required=True)
    parser.add_argument("-o", "--output_path", type=str,
                        help="Path to store output file at.", required=True)
    parser.add_argument("-l", "--languages", type=str,
                        help="Languages to operate on", required=True)
    parser.add_argument("--gerbil_eval", action=argparse.BooleanOptionalAction,
                        help='To perform Gerbil evaluation or not.')
    parser.add_argument("--translate_target_lang", type=str, 
                        help="Target language to translate the input question to. (Translation is enabled only if this value is provided)",
                        default=None, required=False)

    args = parser.parse_args()
    
    # Test QALD file is loaded to json here
    test_file = read_json(args.test)
    # Test QALD file converted to object and preprocessed
    test_qald = Qald(test_file, args.knowledge_graph)
    
    systems = args.systems.split(",")
    
    languages = args.languages.split(",")
    # Output path
    pred_path = args.output_path
    os.makedirs(pred_path, exist_ok=True)
    
    # Gerbil experiments
    gerbil_dict = dict()
    try:
        # For each language
        for language in languages:
            language = language.strip()
            # Question string is extracted alongside its id. This is where features like linguistic context and entity knowledge are extracted
            question_list = test_qald.get_id_question_list(
                language=language,
                include_linguistic_context=False,
                include_entity_knowledge=False,
                question_padding_length=0,
                entity_padding_length=0,
                use_gold_ents=False,
                translate_target_lang=args.translate_target_lang
                )
            # Loop through the systems
            for system_id in systems:
                system_info = SYSTEM_DICT[system_id]
                sys_supported_langs = system_info['langs']
                target_lang = args.translate_target_lang
                # Check if system supports the language or target translation language or system does not support the mentioned knowledge graph
                effective_lang = target_lang if target_lang else language
                if effective_lang not in sys_supported_langs or system_info['kg'] != Knowledge_graph[args.knowledge_graph]:
                    continue
                # Creating QALD dataset object for the predictions
                pred_qald = Qald({}, args.knowledge_graph, True)
                # Iterating through each question to predict its SPARQL
                print('Generating SPARQLs for %s in %s language' % (system_id,language))
                for id, question_string in tqdm(question_list):
                    pred_sparql = extract_sparql(question_string, effective_lang, system_id)
                    pred_qald.add_entry(id,
                                        language,
                                        question_string,
                                        pred_sparql)
                # Fetching results from SPARQL endpoint
                print('Updating answers for %s' % language)
                for qald_entry in tqdm(pred_qald.entries):
                    qald_entry.update_answer()
                    time.sleep(1)
                
                # creating prediction file
                external_pred_path = f"{pred_path}/{system_id}"
                os.makedirs(external_pred_path, exist_ok=True)
                exp_det_file = f"{external_pred_path}/exp_det_{language}"
                # Extract the SPARQL execution details and write to the file
                empty_count = 0
                empty_ids = []
                exception_count = 0
                exception_ids = []
                for qald_entry in pred_qald.entries:
                    query_exec_info = qald_entry.query_exec_info
                    if query_exec_info:
                        if query_exec_info['empty_endpoint_result']:
                            empty_ids.append(query_exec_info['id'])
                            empty_count+= 1
                        elif query_exec_info['sparql_exception']:
                            exception_ids.append(query_exec_info['id'])
                            exception_count+= 1

                with open(exp_det_file, 'w') as exp_det:
                    exp_det.write(f'Number of empty answers from endpoint:{empty_count}' + '\n')
                    exp_det.write(f'Questions with empty answers from endpoint:{empty_ids}' + '\n')
                    exp_det.write(f'Number of SPARQLs causing exceptions:{exception_count}' + '\n')
                    exp_det.write(f'Questions with SPARQL exceptions:{exception_ids}' + '\n')
                    
                # Output file
                output_file = f"{external_pred_path}/{language}.json"
                # Exporting the predicted SPARQL and fetched answers in QALD format
                pred_qald.export_qald_json([language], output_file)
                
                # Move on to next iteration is gerbil evaluation is not required
                if not args.gerbil_eval:
                    continue
                # Gerbil evaluation
                print('Uploading results to Gerbil for %s' % language)
                ref_file = args.test
                ref_file_label = "QALD_9_plus Test"
                model_name = system_id
                # Initializing Gerbil object
                gerbil = Gerbil()
                gerbil.add_ref_file(ref_file_label, ref_file)
                gerbil.add_pred_file(f"{model_name}-{language}", output_file, language)
                response = gerbil.submit_experiment(language)
                print(response)
                # exp_uri_file = f"{pred_path}/exp_uri_{language}"
                # Write the experiment URI to a file
                if response and response.text:
                    print('Gerbil response %s' % response.text)
                    exp_id = response.text
                    exp_id = "https://gerbil-qa.aksw.org/gerbil/experiment?id=" + exp_id.strip()
                    with open(exp_det_file, 'a') as exp_det:
                        exp_det.write(exp_id + '\n')
                # Save gerbil object for export later
                if system_id not in gerbil_dict.keys():
                    gerbil_dict[system_id] = {}
                gerbil_dict[system_id][language] = gerbil
    except Exception as e:
        print('Exception occurred for %s in %s' % (system_id, language))
        # print(str(e))
        traceback.print_exc() 
    finally:
        # Export the Gerbil result files
        for system_id in gerbil_dict:
            for key in gerbil_dict[system_id]:
                result_file_name = f"{pred_path}/{system_id}/result_{key}.csv"
                gerbil : Gerbil = gerbil_dict[system_id][key]
                # Export results to a csv
                gerbil.export_results(result_file_name)

if __name__ == "__main__":
    main()
