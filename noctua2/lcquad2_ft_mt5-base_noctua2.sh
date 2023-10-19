#!/bin/bash

# Sample usage: bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc-ent" 60000
# Sample usage: bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "simple" 60005
# Sample usage: bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc" 60010
# Sample usage: bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "ent" 60015
# Sample usage: bash noctua2/lcquad2_ft_mt5-base_noctua2.sh "lc-ent-noisy" 60001


TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="google/mt5-xl"
TRAIN_FILE="datasets/lcquad2/train-${TRAIN_POSTFIX}.csv"
RUN_NAME="lcquad2-finetune_mt5-base_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
TRAIN_EPOCHS=15
SAVE_STEPS=1000

echo Starting training for: $RUN_NAME

# Queue the job now
#sbatch --job-name=$RUN_NAME --time=60:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS

# Queue the job later
sbatch --begin=now+4hour --job-name=$RUN_NAME --time=60:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS