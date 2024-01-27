#!/bin/bash

## Sample usage: 
# bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc-ent" 60000
# bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "simple" 60005
# bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc" 60010
# bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "ent" 60015

## Noisy sample:
# bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc-ent-noisy" 60001


TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="google/mt5-xl"
TRAIN_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}_train_90pct.csv"
## To enable eval logic
EVAL_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}_dev_10pct.csv"
## To disable eval logic
#EVAL_FILE="false"
RUN_NAME="lcquad2-finetune_mt5-base_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
#TRAIN_EPOCHS=15
## High train epochs for eval based training (early stopping is active)
TRAIN_EPOCHS=300
SAVE_STEPS=1000
BATCH_SIZE=16


echo Starting training for: $RUN_NAME
## Start the job later
#DELAY="+4hour"
## Start the job now
DELAY=""

# Queue the job later
sbatch --begin=now$DELAY --job-name=$RUN_NAME --time=60:00:00 noctua2/noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $EVAL_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $BATCH_SIZE $SAVE_STEPS