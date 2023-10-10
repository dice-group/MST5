import argparse
from utils.data_io import read_json
from dataset.LCquad1 import LCquad1
from dataset.LCquad2 import LCquad2
from dataset.Qald import Qald
from components.Knowledge_graph import Knowledge_graph
from components.Language import Language
from components.Question import Question
from transformers import T5Tokenizer

def get_lcquad_dataset(input_file, dataset_type):
    if dataset_type == "lcquad1":
        return LCquad1(input_file)
    elif dataset_type == "lcquad2":
        return LCquad2(input_file)
    
def get_only_supported_languages(languages):
    supported_languages = []
    for language in languages:
        if Language.has_member_key(language):
            supported_languages.append(language)
    return supported_languages
    
def main():
    parser = argparse.ArgumentParser(
        description="A program to convert qald 9 questions and queries to csv dataset")

    parser.add_argument("-i", "--input", type=str,
                        help="name of input file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("-t", "--type", type=str,
                        help="type of input file", required=True)
    parser.add_argument("-kg", "--knowledge_graph", type=str,
                        help="type of knowledge_graph", required=False)
    parser.add_argument("-l", "--languages", nargs='+',
                        help='required languages of question', required=False)
    parser.add_argument('--linguistic_context', action=argparse.BooleanOptionalAction,
                        help='With or without linguistic context in question string')
    parser.add_argument('--entity_knowledge', action=argparse.BooleanOptionalAction,
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
    
    # Initialize global tokenizer
    Question.lm_tokenizer = T5Tokenizer.from_pretrained('google/mt5-xl', legacy=False)
    Question.lm_tokenizer.add_tokens(["<start-of-pos-tags>", "<start-of-dependency-relation>", "<start-of-dependency-tree-depth>", "<start-of-entity-info>"])

    input_file = read_json(args.input)
    dataset_type = args.type
    if "lcquad" in dataset_type:
        dataset = get_lcquad_dataset(input_file, dataset_type)
        dataset.export_train_csv(
            args.output, 
            args.linguistic_context, 
            args.entity_knowledge,
            args.question_padding_length,
            args.entity_padding_length
            )
    if dataset_type == "qald":
        dataset = Qald(input_file, args.knowledge_graph)
        if args.languages[0]=="all":
            languages = [language.value for language in Language]
            if args.linguistic_context:
                languages.remove("hy")
        else:
            languages = get_only_supported_languages(args.languages)
        dataset.export_train_csv(
        args.output, 
        languages,
        include_linguistic_context=args.linguistic_context,
        include_entity_knowledge=args.entity_knowledge,
        question_padding_length=args.question_padding_length,
        entity_padding_length=args.entity_padding_length
    )





if __name__ == "__main__":
    main()
