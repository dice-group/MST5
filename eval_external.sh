#!/bin/bash
## Sample usage: bash run_eval.sh deeppavlov2023,qanary datasets/qald10/qald_10.json predictions_external_qald10_test en,ru true Wikidata en
## Sample usage: bash run_eval.sh ganswer,tebaqa datasets/qald9plus/dbpedia/qald_9_plus_test_dbpedia.json predictions_external_qald9plus_test en false DBpedia
set -eu

# Setting variables
SYSTEMS=$1
TEST_FILE=$2
OUTPUT_DIR=$3
LANGS=$4
GERBIL_EVAL=$5
KNOWLEDGE_GRAPH=$6
TRANSLATE_TARGET_LANG=${7:-} # Optional argument

# Running the Python script with the provided arguments
python code/eval_external_kgqa_qald.py \
      --systems $SYSTEMS \
      -t $TEST_FILE \
      --knowledge_graph $KNOWLEDGE_GRAPH \
      -o "${OUTPUT_DIR}" \
      -l $LANGS \
      $( [ "$GERBIL_EVAL" = "true" ] && echo "--gerbil_eval" ) \
      ${TRANSLATE_TARGET_LANG:+--translate_target_lang ${TRANSLATE_TARGET_LANG}} \
      2>&1


