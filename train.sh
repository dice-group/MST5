#!/bin/bash

run_name="mt5-base-qald9-dbpedia"
model_name="google/mt5-base"
output_dir="fine-tuned_models/${run_name}"
train_file="datasets/qald9plus/dbpedia/qald_9_plus-train-dbpedia.csv"

CUDA_VISIBLE_DEVICES=1 python train.py \
    --model_name_or_path "google/mt5-base" \
    --do_train \
    --train_file ${train_file} \
    --output_dir ${output_dir} \
    --num_train_epochs 100 \
    --per_device_train_batch_size=8 \
    --overwrite_output_dir \
    --save_steps 10000 \
    --save_total_limit 2 \
    --report_to wandb \
    --run_name ${run_name}
    
