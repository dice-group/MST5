#!/bin/bash

run_name="lcquad-lc-ek-pad-dbp"
model_name="google/mt5-xl"
output_dir="pre-trained_models/${run_name}"
train_file="datasets/lcquad1/train-data.csv"

deepspeed --include=localhost:1 --master_port 61000 code/train_new.py \
    --deepspeed deepspeed/ds_config_zero3.json \
    --model_name_or_path ${model_name} \
    --do_train \
    --train_file ${train_file} \
    --output_dir ${output_dir} \
    --num_train_epochs 32 \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps 1000 \
    --save_total_limit 2 \
    --report_to wandb \
    --run_name ${run_name}\
    --tf32 1 \
    --fp16 0 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4

    # for testing
    # --max_train_samples 100 \
    # --max_eval_samples 20
