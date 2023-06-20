import argparse
from utils.data_io import read_json
from utils.Qald import Qald

supported_languages = [
    "en",
    "de",
    "fr",
    "ru",
    "uk",
    "lt",
    "be",
    "ba",
    "hy",
    "zh",
    "ja"
]


def check_languages(args):
    unsupported_languages = [
        i for i in args.languages if i not in supported_languages]
    languages = [i for i in args.languages if i in supported_languages]
    if len(unsupported_languages) == 1:
        print(", ".join(unsupported_languages) +
              " is not supported by "+args.input)
    if len(unsupported_languages) > 1:
        print(", ".join(unsupported_languages) +
              " are not supported by "+args.input)
    return languages


def main():
    parser = argparse.ArgumentParser(
        description="A program to convert qald 9 questions and queries to csv dataset")

    parser.add_argument("-i", "--input", type=str,
                        help="name of input file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("-l", "--languages", nargs='+',
                        help='required languages of question', required=True)
    parser.add_argument('--linguistic_context', default=False, type=bool,
                        help='With or without linguistic context in question string')
    parser.add_argument('--entity_knowledge', default=False, type=bool,
                        help='With or without entity knowledge in question string')


    args = parser.parse_args()

    languages = check_languages(args)

    qald_file = read_json(args.input)
    qald_dataset = Qald(qald_file)
    qald_dataset.export_train_csv(
        args.output, 
        languages,
        include_linguistic_context=args.linguistic_context,
        include_entity_knowledge=args.entity_knowledge
    )


if __name__ == "__main__":
    main()
