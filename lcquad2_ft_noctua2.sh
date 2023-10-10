#!/bin/bash

# Sample usage: lcquad_ft_noctua2.sh "lc-ent" 60000

TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="google/mt5-xl"
TRAIN_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}.csv"
OUTPUT_DIR="fine-tuned_models/lcquad2-finetune-${TRAIN_POSTFIX}"
RUN_NAME="lcquad2-finetune-${TRAIN_POSTFIX}"
TRAIN_EPOCHS=15
SAVE_STEPS=1000

echo Starting training for: $RUN_NAME

sbatch noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS