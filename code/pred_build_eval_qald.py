import argparse
from utils.data_io import read_json
from dataset.Qald import Qald
from tqdm import tqdm
from components.Summarizer import Summarizer
from components.Text_Generator import Text_Generator
from components.Question import Question
import time
from transformers import T5Tokenizer
import os
from components.Gerbil import Gerbil

def main():
    parser = argparse.ArgumentParser(
        description="A program to use trained model to predict query, build qald dataset and evaluate predictions.")

    parser.add_argument("--model", type=str,
                        help="Path to model (without trailing /)", required=True)
    parser.add_argument("-t", "--test", type=str,
                        help="Name of test file.", required=True)
    parser.add_argument("--knowledge_graph", type=str,
                        help="Type of knowledge_graph.", required=True)
    parser.add_argument("-o", "--output_path", type=str,
                        help="Path to store output file at.", required=True)
    parser.add_argument("-l", "--languages", type=str,
                        help="Languages to operate on", required=True)
    parser.add_argument("--linguistic_context", action=argparse.BooleanOptionalAction,
                        help='With or without linguistic context in question string.')
    parser.add_argument("--entity_knowledge", action=argparse.BooleanOptionalAction,
                        help='With or without entity knowledge in question string.')
    parser.add_argument("--question_padding_length", type=int, 
                        help="length of question string and every linguistic context after padding. \
                        If not provided, no padding will be added.",
                        default=0)
    parser.add_argument("--entity_padding_length", type=int,
                        help="Length of entity knowledge after padding. \
                        If not provided, no padding will be added.",
                        default=0)
    parser.add_argument("--gerbil_eval", action=argparse.BooleanOptionalAction,
                        help='To perform Gerbil evaluation or not.')
    parser.add_argument("--use_gold_ents", action=argparse.BooleanOptionalAction,
                        help='To use gold entities from the reference SPARQL or not.')

    args = parser.parse_args()
    
    # Initialize global tokenizer
    Question.lm_tokenizer = T5Tokenizer.from_pretrained('google/mt5-xl', legacy=False)
    Question.lm_tokenizer.add_tokens(["<start-of-pos-tags>", "<start-of-dependency-relation>", "<start-of-dependency-tree-depth>", "<start-of-entity-info>"])
    # Test QALD file is loaded to json here
    test_file = read_json(args.test)
    # Test QALD file converted to object and preprocessed
    test_qald = Qald(test_file, args.knowledge_graph)
    # Loading model as transformer pipeline
    # As per our experiments, it does not matter whether we use summarization or text2text-generation. We use text2text-generation because it does not complain regarding output length being higher than input.
    # generator = Summarizer(args.model)
    generator = Text_Generator(args.model)
    
    languages = args.languages.split(",")
    # Output path
    pred_path = args.output_path
    
    # Gerbil experiments
    gerbil_dict = dict()
    try:
        # For each language
        for language in languages:
            language = language.strip()
            # Question string is extracted alongside its id. This is where features like linguistic context and entity knowledge are extracted
            question_list = test_qald.get_id_question_list(
                language,
                args.linguistic_context,
                args.entity_knowledge,
                args.question_padding_length,
                args.entity_padding_length,
                args.use_gold_ents
                )
            # Creating QALD dataset object for the predictions
            pred_qald = Qald({}, args.knowledge_graph, True)
            # Iterating through each question to predict its SPARQL
            print('Generating SPARQLs for %s' % language)
            for id, question_string in tqdm(question_list):
                pred_sparql = generator.predict_sparql(question_string)
                pred_qald.add_entry(id,
                                    language,
                                    question_string,
                                    pred_sparql)
            # Fetching results from SPARQL endpoint
            print('Updating answers for %s' % language)
            for qald_entry in tqdm(pred_qald.entries):
                qald_entry.update_answer()
                time.sleep(1)
            # Output file
            output_file = f"{pred_path}/{language}.json"
            # Exporting the predicted SPARQL and fetched answers in QALD format
            pred_qald.export_qald_json([language], output_file)
            
            # Move on to next iteration is gerbil evaluation is not required
            if not args.gerbil_eval:
                continue
            # Gerbil evaluation
            print('Uploading results to Gerbil for %s' % language)
            ref_file = args.test
            ref_file_label = "QALD_9_plus Test"
            model_name = args.model.split(os.sep)[-1].strip()
            # Initializing Gerbil object
            gerbil = Gerbil()
            gerbil.add_ref_file(ref_file_label, ref_file)
            gerbil.add_pred_file(f"{model_name}-{language}", output_file, language)
            response = gerbil.submit_experiment(language)
            print(response)
            exp_uri_file = f"{pred_path}/exp_uri_{language}"
            # Write the experiment URI to a file
            if response and response.text:
                print('Gerbil response %s' % response.text)
                exp_id = response.text
                exp_id = "https://gerbil-qa.aksw.org/gerbil/experiment?id=" + exp_id.strip()
                with open(exp_uri_file, 'w') as exp_det:
                    exp_det.write(exp_id + '\n')
            # Save gerbil object for export later
            gerbil_dict[language] = gerbil
    finally:
        # Export the Gerbil result files
        for key in gerbil_dict:
            result_file_name = f"{pred_path}/result_{key}.csv"
            gerbil : Gerbil = gerbil_dict[key]
            # Export results to a csv
            gerbil.export_results(result_file_name)

if __name__ == "__main__":
    main()
