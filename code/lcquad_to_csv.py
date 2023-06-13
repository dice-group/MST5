import argparse
from utils.process_query import *
from utils.data_io import export_csv


def get_question(lcqald_dict):
    return lcqald_dict["NNQT_question"].replace("{", "").replace("}", "").replace("<", "").replace(">", "")


def get_query(lcqald_dict, kg):
    if kg == "wikidata":
        return lcqald_dict["sparql_wikidata"]
    else:
        return lcqald_dict["sparql_dbpedia18"]


def get_question_query_list(lcquad_entries, kg):
    question_query_list = [["question", "query"]]
    for lcquad_entry in lcquad_entries:
        ques_str = preprocess_nnqt_question(lcquad_entry["NNQT_question"])
        query = get_query(lcquad_entry, kg)
        query = replace_prefix_abbr(delete_sparql_prefix(query))
        question_query_list.append([ques_str, query])
    return question_query_list


def main():
    parser = argparse.ArgumentParser(
        description="A program to extract lcqald questions and queries to csv dataset")

    parser.add_argument("knowledge_graph", choices=[
                        "wikidata", "dbpedia"], help="choose the knowledge graph", default="wikidata")
    parser.add_argument("-i", "--input", type=str, help="name of input file")
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", default="lcqald.csv")

    args = parser.parse_args()

    lcqald_dataset = read_json(args.input)
    lcqald_entry_gen = (lcqald_entry for lcqald_entry in lcqald_dataset)
    question_query_list = get_question_query_list(
        lcqald_entry_gen, args.knowledge_graph)
    export_csv(args.output, question_query_list)


if __name__ == "__main__":
    main()
