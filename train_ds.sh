#!/bin/bash

dataset_name="q9pp-ling-context"
model_name="fine-tuned_models/LC-QuAD"
output_dir="fine-tuned_models/${dataset_name}"
run_name="${model_name}-${dataset_name}"
train_file="datasets/q9pp_ling_context.csv"

deepspeed --include=localhost:1 --master_port 60000 code/train_new.py \
    --deepspeed deepspeed/ds_config_zero3.json \
    --model_name_or_path ${model_name} \
    --do_train \
    --train_file ${train_file} \
    --output_dir ${output_dir} \
    --num_train_epochs 15 \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps 500 \
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
