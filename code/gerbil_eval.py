"""GERBIL Evaluation for QA systems."""
from utils.gerbil import *
import os
import argparse

gold_name = 'qald 9 plus test'
gold_file_path = "datasets/qald9plus/qald_9_pp_test_wikidata.json"

def main():
    parser = argparse.ArgumentParser(
        description="A script to run gerbil experiments")

    # add arguments to the parser
    parser.add_argument("--exp_setting", type=str,
                        help="experiment setting", required=True)
    parser.add_argument("--pred_pfad", type=str,
                        help="pfad of prediction files", required=True)

    args = parser.parse_args()

    exp_setting = args.exp_setting + " "
    pred_pfad = args.pred_pfad
    output_file = pred_pfad + "results.csv"

    languages = [f.split(".")[0] for f in os.listdir(pred_pfad) if f.endswith('.json')]

    upload_gold(gold_name, gold_file_path)
    upload_pred(exp_setting, pred_pfad, languages)

    # set experiment data
    gold = {gold_name: gold_file_path.split('/')[-1]}

    pred = dict()
    for lang in languages:
        pred[exp_setting + lang] = lang + '.json'

    experiment_id = run_experiment(gold, pred).text
    print(f"Experiment id: {experiment_id}")
    gerbil_html = get_html_data(experiment_id)
    if gerbil_html is not None:
        get_results(gerbil_html, output_file)
    else: 
        print("Error when getting GERBIL results")

if __name__ == "__main__":
    # call the main function
    main()
