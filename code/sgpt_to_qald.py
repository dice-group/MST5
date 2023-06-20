from utils.Sgpt import Sgpt
import argparse
from utils.data_io import read_json

def main():
    parser = argparse.ArgumentParser(
        description="A program to convert qald 9 questions and queries to csv dataset")

    parser.add_argument("-i", "--input", type=str,
                        help="path of input file", required=True)
    parser.add_argument("-o_pred", "--output_pred", type=str,
                        help="path of output prediction qald file", required=True)
    parser.add_argument("-o_ref", "--output_ref", type=str,
                    help="path of output reference qald file", required=True)
    
    args = parser.parse_args()

    sgpt_file: list = read_json(args.input)

    Sgpt_dataset: Sgpt = Sgpt(sgpt_file)

    Sgpt_dataset.build_and_extract_pred_qald(args.output_pred)
    Sgpt_dataset.build_and_extract_ref_qald(args.output_ref)
if __name__ == "__main__":
    main()

