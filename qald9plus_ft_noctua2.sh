#!/bin/bash

# Sample usage: qald9plus_ft_noctua2.sh "lc-ent" 60000

TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="fine-tuned_models/lcquad2-finetune-${TRAIN_POSTFIX}"
TRAIN_FILE="datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-${TRAIN_POSTFIX}.csv"
OUTPUT_DIR="fine-tuned_models/qald9plus-finetune-${TRAIN_POSTFIX}"
RUN_NAME="qald9plus-finetune-${TRAIN_POSTFIX}"
TRAIN_EPOCHS=32
SAVE_STEPS=1000

echo Starting training for: $RUN_NAME

sbatch noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS