import argparse
import csv
import json
from preprocess import read_json, replace_prefix_abbr, delete_sparql_prefix

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
    "es"
]


def get_question_query_list(data, languages):
    question_query_list = []

    questions_list = data["questions"]

    for question_dict in questions_list:
        for question in question_dict["question"]:
            query = replace_prefix_abbr(
                delete_sparql_prefix(question_dict["query"]["sparql"]))
            if question["language"] in languages:
                question_query_list.append([question["string"], query])
    return question_query_list


def extract_csv(output_file, question_query_list):
    question_query_list.insert(0, ['question, query'])
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(question_query_list)
    f.close()


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
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A program to convert qald 9 questions and queries to csv dataset")

    # add arguments to the parser
    parser.add_argument("-i", "--input", type=str,
                        help="name of input file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("-l", "--languages", nargs='+',
                        help='required languages of question', required=True)

    # parse the arguments
    args = parser.parse_args()

    languages = check_languages(args)

    qald_dataset = read_json(args.input)
    question_query_list = get_question_query_list(qald_dataset, languages)
    extract_csv(args.output, question_query_list)


# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()
