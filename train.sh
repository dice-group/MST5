#!/bin/bash

set -eu

export WANDB_PROJECT="MST5"

# Port to be used by deepspeed
PORT=$1
# Name of the model to fine-tune
MODEL_NAME=$2
# Path to the training file
TRAIN_FILE=$3
# Path to the eval file
EVAL_FILE=$4
# Output directory to save the fine-tuned model (and checkpoints)
OUTPUT_DIR=$5
# Name of the run to be used for wandb
RUN_NAME=$6
# Number of epochs to train
# Note: As the early stopping mechanism is enabled, train epochs should be kept high. The model will stop training when it starts to overfit.
#TRAIN_EPOCHS=300
TRAIN_EPOCHS=32
# Batch size per device
BATCH_SIZE=$7

# interval in training steps to save the model checkpoints
SAVE_STEPS=1000

# --load_best_model_at_end \
# --do_eval \
# --evaluation_strategy "steps" \
# --eval_steps 50 \
# --eval_delay 0 \
# --validation_file $EVAL_FILE \

# change the --include argument value to state the GPU device to use.
deepspeed --include=localhost:0,1 --master_port $PORT code/train_new.py \
    --deepspeed deepspeed/ds_config_zero2.json \
    --model_name_or_path $MODEL_NAME \
    --do_train \
    --train_file $TRAIN_FILE \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs $TRAIN_EPOCHS \
    --per_device_train_batch_size $BATCH_SIZE \
    --per_device_eval_batch_size $BATCH_SIZE \
    --overwrite_output_dir \
    --save_strategy "steps" \
    --save_steps $SAVE_STEPS \
    --save_total_limit 100 \
    --report_to wandb \
    --run_name $RUN_NAME \
    --logging_steps 10 \
    --tf32 1 \
    --fp16 0 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4
    
