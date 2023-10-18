#!/bin/bash

set -eu

export WANDB_PROJECT="MST5"

# Port to be used by deepspeed
PORT=$1
# Name of the model to fine-tune
MODEL_NAME=$2
# Path to the training file
TRAIN_FILE=$3
# Output directory to save the fine-tuned model (and checkpoints)
OUTPUT_DIR=$4
# Name of the run to be used for wandb
RUN_NAME=$5
# Number of epochs to train
TRAIN_EPOCHS=$6
# interval in training steps to save the model checkpoints
SAVE_STEPS=$7



deepspeed --include=localhost:0 --master_port $PORT code/train_new.py \
    --deepspeed deepspeed/ds_config_zero2.json \
    --model_name_or_path $MODEL_NAME \
    --do_train \
    --train_file $TRAIN_FILE \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs $TRAIN_EPOCHS \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps $SAVE_STEPS \
    --save_total_limit 1 \
    --report_to wandb \
    --run_name $RUN_NAME \
    --logging_steps 10 \
    --tf32 1 \
    --fp16 0 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4
    
