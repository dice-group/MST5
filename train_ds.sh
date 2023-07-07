#!/bin/bash

run_name="exp13-mt5xl-lcquad-lc-ptek-pad-dbp-endefr"
model_name="pre-trained_models/lcquad-lc-ek-pad-dbp"
output_dir="fine-tuned_models/${run_name}"
train_file="datasets/qald9plus/dbpedia/qald_9_plus-train_dbpedia.csv"

deepspeed --include=localhost:0 --master_port 60000 code/train_new.py \
    --deepspeed deepspeed/ds_config_zero3.json \
    --model_name_or_path ${model_name} \
    --do_train \
    --train_file ${train_file} \
    --output_dir ${output_dir} \
    --num_train_epochs 15 \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps 600 \
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
