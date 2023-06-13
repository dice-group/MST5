import argparse
from utils.qald import get_question_query_list
from utils.data_io import read_json, export_csv

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
    "es",
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
    parser.add_argument('--linguistic', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    languages = check_languages(args)

    qald_dataset = read_json(args.input)
    question_query_list = get_question_query_list(
        qald_dataset, languages, args.linguistic)
    export_csv(args.output, question_query_list)


if __name__ == "__main__":
    main()
