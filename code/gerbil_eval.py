"""GERBIL Evaluation for QA systems."""
from utils.gerbil import *
import os

folder_path = "pred_files/mt5/4_mt5/"

languages = [f.split(".")[0] for f in os.listdir(folder_path) if f.endswith('.json')]

gold_name = 'qald 9 plus test'
gold_file_path = "datasets/qald9plus/qald_9_pp_test_wikidata.json"

exp_setting = "four-shot mt5 "
pred_pfad_prefix = "pred_files/mt5/4_mt5/"
output_file = pred_pfad_prefix + "results.csv"


upload_gold(gold_name, gold_file_path)
upload_pred(exp_setting, pred_pfad_prefix, languages)

# set experiment data
gold = {gold_name: gold_file_path.split('/')[-1]}

pred = dict()
for lang in languages:
    pred[exp_setting + lang] = lang + '.json'

experiment_id = run_experiment(gold, pred).text
gerbil_html = get_html_data(experiment_id)
if gerbil_html is not None:
    get_results(gerbil_html, output_file)
else: 
    print("Error when getting GERBIL results")