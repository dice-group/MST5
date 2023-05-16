import argparse
import re
import spacy
from utils.preprocess import read_json
from utils.linguistic_parser import get_doc, get_pos, get_dep, get_root_node, get_dep_depth
from utils.export import export_json

nlp_en = spacy.load("en_core_web_sm")
nlp_zh = spacy.load("zh_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")
nlp_ja = spacy.load("ja_core_news_sm")
nlp_lt = spacy.load("lt_core_news_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_ru = spacy.load("ru_core_news_sm")
nlp_uk = spacy.load("uk_core_news_sm")
nlp_es = spacy.load("es_core_news_sm")

nlp_dict = {
    "en": nlp_en,
    "zh": nlp_zh,
    "de": nlp_de,
    "fr": nlp_fr,
    "ja": nlp_ja,
    "lt": nlp_lt,
    "es": nlp_es,
    "uk": nlp_uk,
    "ru": nlp_ru,
    "ba": nlp_ru,
    "be": nlp_ru
}

def preprocess_nnqt_question(NNQT_ques):
    # Remove all specified characters
    NNQT_ques = NNQT_ques.translate(str.maketrans('<>{},()', '       '))
    
    # Replace multiple spaces with a single space
    NNQT_ques = re.sub(' +', ' ', NNQT_ques)
    
    return NNQT_ques
def add_to_lcquad(dataset, nlp, output):
    for ques_dict in dataset:
        ques = preprocess_nnqt_question(ques_dict["NNQT_question"])
        pos, dep, depth_list = get_linguistic_context(nlp, ques)
        ques_dict["pos"] = pos
        ques_dict["dep"] = dep
        ques_dict["dep_depth"] = depth_list
    export_json(output, dataset)

def get_linguistic_context(nlp, ques):
    doc = get_doc(ques, nlp)
    pos = get_pos(doc)
    dep = get_dep(doc)
    root = get_root_node(doc, dep)
    depth_list = get_dep_depth(root, [-1] * len(doc))
    return doc, pos, dep, depth_list

def add_to_qald(dataset, output):
    for ques_dict in dataset["questions"]:
        for ques_str_dict in ques_dict["question"]:
            language = ques_str_dict["language"]
            ques_str = ques_str_dict["string"]
            if language != "hy":
                nlp = nlp_dict.get(language)
                doc, pos, dep, depth_list = get_linguistic_context(nlp, ques_str) 
                ques_str_dict["doc"] = [token.text for token in doc]
                ques_str_dict["pos"] = pos
                ques_str_dict["dep"] = dep
                ques_str_dict["dep_depth"] = depth_list
    export_json(output, dataset)

def main():
    parser = argparse.ArgumentParser(
        description="A program to convert qald 9 questions and queries to csv dataset")

    # add arguments to the parser
    parser.add_argument("-i", "--input", type=str,
                        help="name of input file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", required=True)
    parser.add_argument("--format", type=str, help="format of dataset, lcquad or qald", required=True)


    args = parser.parse_args()
    dataset = read_json(args.input)

    if args.format == "lcquad":
        nlp = spacy.load("en_core_web_sm")
        add_to_lcquad(dataset, nlp, args.output)
    elif args.format == "qald":
        add_to_qald(dataset, args.output)
    else:
        print("File format is not supported")

if __name__ == "__main__":
    # call the main function
    main()

