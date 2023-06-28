import argparse
from utils.data_io import read_json
from dataset.LCquad1 import LCquad1


def main():
    parser = argparse.ArgumentParser(
        description="A program to extract lcqald questions and queries to csv dataset")

    parser.add_argument("-i", "--input", type=str, help="name of input file")
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", default="lcqald.csv")
    parser.add_argument('--linguistic_context', default=False, type=bool,
                        help='With or without linguistic context in question string')
    parser.add_argument('--entity_knowledge', default=False, type=bool,
                        help='With or without entity knowledge in question string')

    args = parser.parse_args()

    lcquad_file = read_json(args.input)
    lcquad_dataset = LCquad1(lcquad_file)
    lcquad_dataset.export_train_csv(args.output, args.linguistic_context, args.entity_knowledge)

if __name__ == "__main__":
    main()
