#!/bin/bash

# Sample usage: bash best_ft_t5-base_noctua2.sh

TRAIN_POSTFIX="lc-ent"
PORT=60040

## To fine-tune on LCQUAD2
# MODEL_NAME="google/t5-efficient-xl"
# TRAIN_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}.csv"
# RUN_NAME="eng-only_lcquad2-finetune_t5-base_${TRAIN_POSTFIX}"
# OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
# TRAIN_EPOCHS=15
# SAVE_STEPS=1000

## To fine-tune on QALD_9_Plus English
# MODEL_NAME="fine-tuned_models/eng-only_lcquad2-finetune_t5-base_${TRAIN_POSTFIX}"
# TRAIN_FILE="datasets/qald9plus/wikidata/en-only_qald_9_plus_train_wikidata-${TRAIN_POSTFIX}.csv"
# RUN_NAME="eng-only_qald9plus-finetune_lcquad2-base_${TRAIN_POSTFIX}"
# OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
# TRAIN_EPOCHS=100
# SAVE_STEPS=200

## To continue fine-tune on QALD_9_Plus English
MODEL_NAME="fine-tuned_models/eng-only_qald9plus-finetune_lcquad2-base_${TRAIN_POSTFIX}"
TRAIN_FILE="datasets/qald9plus/wikidata/en-only_qald_9_plus_train_wikidata-${TRAIN_POSTFIX}.csv"
RUN_NAME="eng-only_qald9plus-finetune_lcquad2-base_300epochs_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
TRAIN_EPOCHS=200
SAVE_STEPS=200

echo Starting training for: $RUN_NAME

sbatch --job-name=$RUN_NAME --time=15:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS  