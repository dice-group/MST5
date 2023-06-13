from utils.gerbil import *
import os
import argparse

ref_name = 'qald 9 plus test'
ref_file_path = "datasets/qald9plus/qald_9_pp_test_wikidata.json"

def main():
    parser = argparse.ArgumentParser(
        description="A script to run gerbil experiments")

    parser.add_argument("--exp_setting", type=str,
                        help="experiment setting", required=True)
    parser.add_argument("--pred_pfad", type=str,
                        help="pfad of prediction files", required=True)

    args = parser.parse_args()

    exp_setting = args.exp_setting + " "
    pred_pfad = args.pred_pfad
    output_file = pred_pfad + "results.csv"

    languages = [f.split(".")[0] for f in os.listdir(pred_pfad) if f.endswith('.json')]

    upload_file(ref_name, ref_file_path, "ref")
    upload_pred_by_lang(exp_setting, pred_pfad, languages)

    # set experiment data
    ref = {ref_name: ref_file_path.split('/')[-1]}

    pred = dict()
    for lang in languages:
        pred[exp_setting + lang] = lang + '.json'

    experiment_id = submit_experiment(ref, pred).text
    print(f"Experiment id: {experiment_id}")
    gerbil_html = get_exp_result_content(experiment_id)
    if gerbil_html is not None:
        gerbil_results_table = clean_gerbil_table(gerbil_html)
        gerbil_results_table.to_csv(output_file, index=False)
        print("Experiment results is saved to " + output_file)
    else: 
        print("Error when getting GERBIL results")

if __name__ == "__main__":
    main()
