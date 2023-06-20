from sklearn.metrics import f1_score
from utils.query import preprocess_sparql
from enum import Enum
import re


class Type(Enum):
    BOOLEAN = "boolean"
    RANK = "rank"
    COUNT = "count"
    SIMPLE = "simple"


class Ques_pair:
    def __init__(self, ques_ref, ques_pred) -> None:
        self.validate_ids(ques_ref, ques_pred)
        self.id = ques_ref["id"]
        self.question_string = ques_ref["question"][0]["string"]
        self.ref_sparql = ques_ref["query"]["sparql"]
        self.pred_sparql = ques_pred["query"]["sparql"]
        self.type = self.detect_query_type()
        self.ref_answer = self.get_answer(ques_ref)
        self.pred_answer = self.get_answer(ques_pred)

    def validate_ids(self, ques_ref, ques_pred):
        if ques_ref["id"] != ques_pred["id"]:
            raise ValueError(
                "predicted question dict doesn't have same id as reference")

    def detect_query_type(self):
        if "ASK" in self.ref_sparql:
            return Type.BOOLEAN
        elif "ORDER" in self.ref_sparql:
            return Type.RANK
        elif "COUNT" in self.ref_sparql:
            return Type.COUNT
        return Type.SIMPLE

    def get_answer(self, ques_dict):
        try:
            return ques_dict["answers"][0]["results"]["bindings"]
        except:
            pass
        try:
            return ques_dict["answers"][0]["boolean"]
        except:
            return []

    def print(self, print_answer=False):
        print("id: " + self.id)
        print("question: " + self.question_string)
        print("ref sparql: " + self.ref_sparql)
        print("pred sparql: " + self.pred_sparql)
        if print_answer:
            print("ref_answer:\n", self.ref_answer)
            print("pred_answer:\n", self.pred_answer)
        print()

    def collect_entities(self):
        ref_entity_list = re.findall(r'wd:[A-Z]*[0-9]*', self.ref_sparql)
        pred_entity_list = re.findall(r'wd:[A-Z]*[0-9]*', self.pred_sparql)
        return ref_entity_list, pred_entity_list

    def collect_relations(self):
        ref_relation_list = re.findall(r'wdt:[A-Z]*[0-9]*', self.ref_sparql)
        pred_relation_list = re.findall(r'wdt:[A-Z]*[0-9]*', self.pred_sparql)
        return ref_relation_list, pred_relation_list

    def calculate_entity_f1(self):
        ref_entity_list, pred_entity_list = self.collect_entities()
        ref_entity_list, pred_entity_list = self.pad_list(
            ref_entity_list, pred_entity_list)
        score = f1_score(ref_entity_list, pred_entity_list, average="macro")
        return score

    def calculate_relation_f1(self):
        ref_relation_list, pred_relation_list = self.collect_relations()
        ref_relation_list, pred_relation_list = self.pad_list(
            ref_relation_list, pred_relation_list)
        score = f1_score(ref_relation_list,
                         pred_relation_list, average="macro")
        return score

    def pad_list(self, ref, pred):
        max_length = max(len(ref), len(pred))
        if len(ref) < max_length:
            ref.extend(["PAD_ref" for _ in range(max_length - len(ref))])
        if len(pred) < max_length:
            pred.extend(["PAD_pred" for _ in range(max_length - len(pred))])
        if ref == [] and pred == []:
            ref, pred = ["PAD_ref"], ["PAD_pred"]
        return ref, pred
