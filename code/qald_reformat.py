import argparse
from utils.preprocess import read_json, replace_prefix_abbr, delete_sparql_prefix
from utils.export import export_csv

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


def get_question_query_list(data, languages, linguistic):
    question_query_list = []

    questions_list = data["questions"]

    for question_dict in questions_list:
        for question in question_dict["question"]:
            query = replace_prefix_abbr(
                delete_sparql_prefix(question_dict["query"]["sparql"]))
            if question["language"] in languages:
                if linguistic:
                    question_linguistic = " ".join(question["doc"]) \
                    + " <pad> " + " ".join(question["pos"]) \
                    + " <pad> " + " ".join(question["dep"]) \
                    + " <pad> " + " ".join(map(str, question["dep_depth"]))
                    question_query_list.append([question_linguistic, query])
                else:
                    question_query_list.append([question["string"], query])
    question_query_list.insert(0, ['question, query'])
    return question_query_list


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
    parser.add_argument('--linguistic', action=argparse.BooleanOptionalAction)

    # parse the arguments
    args = parser.parse_args()

    languages = check_languages(args)

    qald_dataset = read_json(args.input)
    question_query_list = get_question_query_list(
        qald_dataset, languages, args.linguistic)
    export_csv(args.output, question_query_list)


# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()
