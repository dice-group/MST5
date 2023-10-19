#!/bin/bash

# Sample usage: bash noctua2/qald10train_ft_lcquad2-ft-base_noctua2.sh "lc-ent" 60020
# Sample usage: bash noctua2/qald10train_ft_lcquad2-ft-base_noctua2.sh "lc-ent-noisy" 60025

TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="fine-tuned_models/lcquad2-finetune_mt5-base_${TRAIN_POSTFIX}"
TRAIN_FILE="datasets/qald10/qald10_train-${TRAIN_POSTFIX}.csv"
RUN_NAME="qald10train-finetune_lcquad2-ft-base_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
TRAIN_EPOCHS=32
SAVE_STEPS=500

echo Starting training for: $RUN_NAME

# Queue the job now
# sbatch --job-name=$RUN_NAME --time=40:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS

# Queue the job later
sbatch --begin=now+10hour --job-name=$RUN_NAME --time=40:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS