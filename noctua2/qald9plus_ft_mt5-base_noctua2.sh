#!/bin/bash

# Sample usage: bash qald9plus_ft_mt5-base_noctua2.sh "lc-ent" 60020
# Sample usage: bash qald9plus_ft_mt5-base_noctua2.sh "simple" 60025
# Sample usage: bash qald9plus_ft_mt5-base_noctua2.sh "lc" 60030
# Sample usage: bash qald9plus_ft_mt5-base_noctua2.sh "ent" 60035

TRAIN_POSTFIX=$1
PORT=$2

MODEL_NAME="google/mt5-xl"
TRAIN_FILE="datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-${TRAIN_POSTFIX}.csv"
RUN_NAME="qald9plus-finetune_mt5-base_${TRAIN_POSTFIX}"
OUTPUT_DIR="fine-tuned_models/${RUN_NAME}"
TRAIN_EPOCHS=32
SAVE_STEPS=1000

echo Starting training for: $RUN_NAME

sbatch --job-name=$RUN_NAME --time=15:00:00 noctua2_train.sh $PORT $MODEL_NAME $TRAIN_FILE $OUTPUT_DIR $RUN_NAME $TRAIN_EPOCHS $SAVE_STEPS