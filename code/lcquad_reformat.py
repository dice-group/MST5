import argparse
import csv
from utils.preprocess import read_json, replace_prefix_abbr, delete_sparql_prefix

def get_question(lcqald_dict):
    return lcqald_dict["NNQT_question"].replace("{", "").replace("}", "").replace("<", "").replace(">", "")


def get_query(lcqald_dict, kg):
    if kg == "wikidata":
        return lcqald_dict["sparql_wikidata"]
    else:
        return lcqald_dict["sparql_dbpedia18"]


def get_question_query(lcqald_dicts, kg, output):
    question_query_list = [["question", "query"]]
    for lcqald_dict in lcqald_dicts:
        question = get_question(lcqald_dict)
        query = get_query(lcqald_dict, kg)
        query = replace_prefix_abbr(delete_sparql_prefix(query))
        question_query_list.append([question, query])
    with open(output, "w") as f:
        writer = csv.writer(f)
        writer.writerows(question_query_list)
    f.close()


def main():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A program to extract lcqald questions and queries to csv dataset")

    # add arguments to the parser
    parser.add_argument("knowledge_graph", choices=[
                        "wikidata", "dbpedia"], help="choose the knowledge graph", default="wikidata")
    parser.add_argument("-i", "--input", type=str, help="name of input file")
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", default="lcqald.csv")

    # parse the arguments
    args = parser.parse_args()

    lcqald = read_json(args.input)
    lcqald_dict_gen = (lcqald_dict for lcqald_dict in lcqald)
    get_question_query(lcqald_dict_gen, args.knowledge_graph, args.output)


# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()
