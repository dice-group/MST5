#!/bin/bash

# Sample usage: bash best_ft_t5-base_noctua2.sh

TRAIN_POSTFIX="lc-ent"
PORT=60040

MODEL_NAME="google/t5-efficient-xl"
TRAIN_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}.csv"
RUN_NAME="eng-only_lcquad2-finetune_t5-base_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
TRAIN_EPOCHS=15
SAVE_STEPS=1000

echo Starting training for: $RUN_NAME

sbatch --job-name=$RUN_NAME --time=35:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS  