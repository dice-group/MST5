import argparse
from utils.data_io import read_json
from dataset.Qald import Qald
from tqdm import tqdm
from components.Summarizer import Summarizer


def main():
    parser = argparse.ArgumentParser(
        description="A program to use model to predict query and build qald dataset")

    parser.add_argument("--model", type=str,
                        help="name of model path", required=True)
    parser.add_argument("-t", "--test", type=str,
                        help="name of test file", required=True)
    parser.add_argument("--knowledge_graph", type=str,
                        help="type of knowledge_graph", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("-l", "--language", type=str,
                        help="required language of question", required=True)
    parser.add_argument("--linguistic_context", action=argparse.BooleanOptionalAction,
                        help='With or without linguistic context in question string')
    parser.add_argument("--entity_knowledge", action=argparse.BooleanOptionalAction,
                        help='With or without entity knowledge in question string')
    parser.add_argument("--question_padding_length", type=int, 
                        help="length of question string and every linguistic context after padding. \
                        If not provided, no padding will be added.",
                        default=0)
    parser.add_argument("--entity_padding_length", type=int,
                        help="length of entity knowledge after padding. \
                        If not provided, no padding will be added.",
                        default=0)

    args = parser.parse_args()

    test_file = read_json(args.test)
    test_qald = Qald(test_file, args.knowledge_graph)
    question_list = test_qald.get_id_question_list(
        args.language,
        args.linguistic_context,
        args.entity_knowledge,
        args.question_padding_length,
        args.entity_padding_length
        )
    summarizer = Summarizer(args.model)
    pred_qald = Qald({}, args.knowledge_graph)
    for id, question_string in tqdm(question_list):
        pred_sparql = summarizer.predict_sparql(question_string)
        pred_qald.add_entry(id,
                            args.language,
                            question_string,
                            pred_sparql)
    # pred_qald.update_answers()
    print('Updating answers for %s' % args.language)
    for qald_entry in tqdm(pred_qald.entries):
            qald_entry.update_answer()
    pred_qald.export_qald_json([args.language], args.output)


if __name__ == "__main__":
    main()
