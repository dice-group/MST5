import os
import argparse
from utils.gerbil import Gerbil

default_ref_name = 'qald 9 plus test'
default_ref_file_path = "datasets/qald9plus/dbpedia/qald_9_plus_test_dbpedia.json"

def main():
    parser = argparse.ArgumentParser(
        description="A script to run gerbil experiments")
    

    parser.add_argument("--ref_name", 
                        type=str,
                        help="name of reference file", 
                        default=default_ref_name,
                        required=False)
    parser.add_argument("--ref_file_path", 
                        type=str,
                        help="path of reference file", 
                        default=default_ref_file_path,
                        required=False)
    parser.add_argument("--experiment_id",
                        type=str,
                        help="Experiment id for which results need to be exported",
                        default=None,
                        required=False)
    parser.add_argument("--exp_setting", type=str,
                        help="experiment setting", required=False)
    parser.add_argument("--pred_path", type=str,
                        help="path of prediction files", required=True)

    args = parser.parse_args()

    gerbil = Gerbil()

    if args.experiment_id:
        gerbil.add_experiment_id(args.experiment_id)
        gerbil.export_results(f"{args.pred_path}/result.csv")
        return

    languages = [f.split(".")[0] for f in os.listdir(args.pred_path) if f.endswith('.json')]
    gerbil.add_ref_file(args.ref_name, args.ref_file_path)
    for lang in languages:
        gerbil.add_pred_file(f"{args.exp_setting}-{lang}", f"{args.pred_path}/{lang}.json", lang)
    gerbil.submit_experiment()
    gerbil.export_results(f"{args.pred_path}/result.csv")

if __name__ == "__main__":
    main()
