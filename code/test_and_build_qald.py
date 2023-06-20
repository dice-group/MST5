import argparse
from utils.data_io import read_json, export_json
from utils.query import init_summarizer, predict_query, ask_wikidata
from utils.process_query import postprocess_sparql
from utils.qald import build_qald_entry
from utils.Qald import Qald
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(
        description="A program to use model to predict query and build qald dataset")

    parser.add_argument("--model", type=str,
                        help="name of model path", required=True)
    parser.add_argument("-t", "--test", type=str,
                        help="name of test file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("-l", "--language", type=str,
                        help="required language of question", required=True)
    parser.add_argument('--linguistic_context', default=False, type=bool,
                        help='With or without linguistic context in question string')
    parser.add_argument('--entity_knowledge', default=False, type=bool,
                        help='With or without entity knowledge in question string')

    args = parser.parse_args()

    test_file = read_json(args.test)
    testset = Qald(test_file)
    summarizer = init_summarizer(args.model)
    question_list = testset.get_question_string_with_id(args.language, args.linguistic_context, args.entity_knowledge)

    result = Qald({})
    for id, question_string in tqdm(question_list):
        query_pred = predict_query(summarizer, question_string)
        sparql_query = postprocess_sparql(query_pred)
        answer = ask_wikidata(sparql_query)
        result.add_entry(id, args.language, question_string, sparql_query, answer)
    result.export_qald_json([args.language], args.output)


if __name__ == "__main__":
    main()
