import argparse
from utils.preprocess import read_json
from utils.query import init_summarizer, predict_query, ask_wikidata
from utils.postprocess import postprocess_sparql
from utils.build_qald import build_qald_entry
from utils.export import export_json
from tqdm import tqdm


def get_question_list_with_id(data, languages, linguisitic_context):
    question_list = []

    questions_list = data["questions"]

    for question_dict in questions_list:
        for question in question_dict["question"]:
            if question["language"] in languages:
                if linguisitic_context:
                    depth_str_list = map(str, question["dep_depth"])
                    question_string = " ".join(question["doc"]) \
                    + "<pad>" + " ".join(question["pos"]) \
                    + "<pad>" + " ".join(question["dep"]) \
                    + "<pad>" + " ".join(depth_str_list) 
                else:
                    question_string = question["string"]
                question_list.append([question_dict["id"], question_string])
                break
    return question_list


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
    parser.add_argument('--linguistic_context', default=False, type=bool, help='With or without linguistic context in question string')

    # parse the arguments
    args = parser.parse_args()

    testset = read_json(args.test)
    summarizer = init_summarizer(args.model)
    question_list = get_question_list_with_id(
        testset, [args.language], args.linguistic_context)

    pred_qald_list = []
    for id, question_string in tqdm(question_list):
        query_pred = predict_query(summarizer, question_string)
        sparql_query = postprocess_sparql(query_pred)
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
