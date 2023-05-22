from sklearn.metrics import f1_score
from utils.preprocess import delete_sparql_prefix, prefix_pattern
from utils.preprocess import read_json
import re
import numpy as np
import pandas as pd
import argparse
import logging

# create logger
logger = logging.getLogger('logger')
logger.setLevel(logging.WARNING)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def replace_prefix_with_abbr(sparql):
    for pattern in prefix_pattern:
        sparql = re.sub(pattern[0], pattern[1]+r'\1', sparql)
    sparql = re.sub(' +', ' ', sparql)
    return sparql

def clean_sparql(sparql):
    return replace_prefix_with_abbr(delete_sparql_prefix(sparql))

class Ques_pair:
    def __init__(self, ques_ref, ques_pred) -> None:
        self.validate_ids(ques_ref, ques_pred)
        self.id = ques_ref["id"]
        self.question_string = ques_ref["question"][0]["string"]
        self.ref_sparql = clean_sparql(ques_ref["query"]["sparql"])
        self.pred_sparql = clean_sparql(ques_pred["query"]["sparql"])
        self.type = self.detect_query_type()
        self.ref_answer = self.get_answer(ques_ref)
        self.pred_answer = self.get_answer(ques_pred)

    def validate_ids(self, ques_ref, ques_pred):
        if ques_ref["id"] != ques_pred["id"]:
            raise ValueError("predicted question dict doesn't have same id as reference")
    
    def detect_query_type(self):
        if "ASK" in self.ref_sparql:
            return "Boolean"
        elif "ORDER" in self.ref_sparql:
            return "Rank"
        elif "COUNT" in self.ref_sparql:
            return "Count"
        return "Simple"
    
    def get_answer(self, ques_dict):
        try:
            return ques_dict["answers"][0]["results"]["bindings"]
        except: 
            pass
        try: 
            return ques_dict["answers"][0]["boolean"]
        except:
            return []
    
    def print(self):
        print("id: " + self.id)
        print("question: " + self.question_string)
        print("ref sparql: " + self.ref_sparql)
        print("pred sparql: " + self.pred_sparql)
        print("ref_answer:\n", self.ref_answer)
        print("pred_answer:\n", self.pred_answer)

    def collect_entities(self):
        ref_entity_list = re.findall(r'wd:[A-Z]*[0-9]*', self.ref_sparql)
        pred_entity_list = re.findall(r'wd:[A-Z]*[0-9]*', self.pred_sparql)
        return ref_entity_list, pred_entity_list
    
    def collect_relations(self):
        ref_relation_list = re.findall(r'wdt:[A-Z]*[0-9]*', self.ref_sparql)
        pred_relation_list = re.findall(r'wdt:[A-Z]*[0-9]*', self.pred_sparql)
        return ref_relation_list, pred_relation_list

    def calculate_entity_f1(self):
        logger.info("Calculate entity F1 score for question id " + self.id)
        ref_entity_list, pred_entity_list = self.collect_entities()
        ref_entity_list, pred_entity_list = self.pad_list(ref_entity_list, pred_entity_list)
        score = f1_score(ref_entity_list, pred_entity_list, average="macro")
        logger.info("Entity F1 score is " + str(score))
        return score

    def calculate_relation_f1(self):
        logger.info("Calculate relation F1 score for question " + self.id)
        ref_relation_list, pred_relation_list = self.collect_relations()
        ref_relation_list, pred_relation_list = self.pad_list(ref_relation_list, pred_relation_list)
        score = f1_score(ref_relation_list, pred_relation_list, average="macro")
        logger.info("Relation F1 score is " + str(score))
        return score

    def pad_list(self, ref, pred):
        max_length = max(len(ref), len(pred))
        if len(ref) < max_length:
            ref.extend(["PAD_ref" for i in range(max_length - len(ref))])
        if len(pred) < max_length:
            pred.extend(["PAD_pred" for i in range(max_length - len(pred))])
        if ref == [] and pred == []:
            ref, pred = ["PAD_ref"], ["PAD_pred"]
        return ref,pred

def main():
    parser = argparse.ArgumentParser(
        description="A script to calculate F1 scores for entity and relations")

    # add arguments to the parser
    parser.add_argument("--ref_file", type=str,
                        help="path of reference file", required=True)
    parser.add_argument("--pred_file", type=str,
                        help="pfad of prediction file", required=True)

    args = parser.parse_args()

    ref_file = read_json(args.ref_file)
    pred_file = read_json(args.pred_file)

    logger.info("loaded ref file " + args.ref_file)
    logger.info("loaded pred file " + args.pred_file)

    ref_list = ref_file["questions"]
    pred_list = pred_file["questions"]

    ques_pair = Ques_pair(ref_list[0], pred_list[0])
    ques_pair.calculate_entity_f1()
    ques_pair.calculate_relation_f1()
    
if __name__ == "__main__":
    main()
