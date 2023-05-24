#!/bin/bash

dataset_name="12"
model_name="fine-tuned_models/lcquad_mt5-xl"
output_dir="fine-tuned_models/lcquad_mt5-xl/${dataset_name}"
run_name="${model_name} ${dataset_name}"

deepspeed code/train_new.py \
    --deepspeed deepspeed/ds_config_zero3.json \
    --model_name_or_path ${model_name} \
    --do_train \
    --do_eval \
    --eval_steps 1500 \
    --train_file datasets/12/q9pp_train.csv \
    --validation_file datasets/1/q9pp_test.csv \
    --output_dir ${output_dir} \
    --num_train_epochs 15 \
    --per_device_train_batch_size=4 \
    --overwrite_output_dir \
    --save_steps 5000 \
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
