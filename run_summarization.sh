#!/bin/bash

dataset_name="11_linguistic"
output_dir="fine-tuned_models/${dataset_name}_mt5"

python run_summarization.py \
    --model_name_or_path "google/mt5-base" \
    --do_train \
    --do_eval \
    --train_file datasets/qald_9_plus/${dataset_name}/q9pp_train.csv \
    --validation_file datasets/qald_9_plus/12/q9pp_test.csv \
    --output_dir ${output_dir} \
    --num_train_epochs 300 \
    --per_device_train_batch_size=4 \
    --overwrite_output_dir \
    --save_steps 30000 \
    --save_total_limit 2
    # --tokenizer_name lcquad_tokenizer \
