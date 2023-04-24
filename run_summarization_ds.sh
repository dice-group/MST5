#!/bin/bash

dataset_name="11_linguistic"
output_dir="fine-tuned_models/${dataset_name}_mt5-xxl"

deepspeed run_summarization.py \
    --deepspeed deepspeed/ds_config_zero3.json \
    --model_name_or_path "google/mt5-xxl" \
    --do_train \
    --train_file datasets/qald_9_plus/${dataset_name}/q9pp_train.csv \
    --output_dir ${output_dir} \
    --num_train_epochs 100 \
    --per_device_train_batch_size=4 \
    --overwrite_output_dir \
    --save_steps 30000 \
    --save_total_limit 3 \
    --report_to wandb \
    --tf32 0 \
    --fp16 1 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4


    # for testing
    # --max_train_samples 100 \
    # --max_eval_samples 20
