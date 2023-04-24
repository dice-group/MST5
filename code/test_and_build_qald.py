import argparse
from utils.preprocess import read_json
from utils.query import init_summarizer, predict_query, ask_wikidata
from utils.preprocess import replace_prefix_abbr, delete_sparql_prefix
from utils.postprocess import postprocessing_sparql
from utils.build_qald import build_qald_entry
from utils.export import export_json


def get_question_query_list_with_id(data, languages):
    question_query_list = []

    questions_list = data["questions"]

    for question_dict in questions_list:
        for question in question_dict["question"]:
            query = replace_prefix_abbr(
                delete_sparql_prefix(question_dict["query"]["sparql"]))
            if question["language"] in languages:
                question_query_list.append(
                    [question_dict["id"], question["string"], query])
                break
    return question_query_list


def main():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A program to use model to predict query and build qald dataset")

    # add arguments to the parser
    parser.add_argument("--model", type=str,
                        help="name of model path", required=True)
    parser.add_argument("-t", "--test", type=str,
                        help="name of test file", required=True)
    parser.add_argument("-o", "--output", type=str, 
                        help="name of output file", required=True)
    parser.add_argument("-l", "--language", type=str,
                        help="required language of question", required=True)

    # parse the arguments
    args = parser.parse_args()

    testset = read_json(args.test)
    summarizer = init_summarizer(args.model)
    question_query_list = get_question_query_list_with_id(
        testset, [args.language])

    pred_qald_list = []
    for id, question_string, _ in question_query_list:
        query_pred = predict_query(summarizer, question_string)
        sparql_query = postprocessing_sparql(query_pred)
        answer = ask_wikidata(sparql_query)
        qald_entry = build_qald_entry(
            id, question_string, sparql_query, answer, args.language)
        pred_qald_list.append(qald_entry)
    qald_pred = {"questions": pred_qald_list}
    export_json(args.output, qald_pred)


# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()
