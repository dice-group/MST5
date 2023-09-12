#!/bin/bash

set -eu
#model_name="google/mt5-xl"
#output_dir="fine-tuned_models/${run_name}"
#train_file="datasets/lcquad2/train.csv"

if [ $# -ne 3 ]
  then
    echo "Please provide the relevant number of arguments!"
    return -1
fi

model_name=$1
output_dir=$2
train_file=$3

CUDA_VISIBLE_DEVICES=1 python train.py \
    --model_name_or_path "google/mt5-base" \
    --do_train \
    --train_file ${train_file} \
    --output_dir ${output_dir} \
    --num_train_epochs 100 \
    --per_device_train_batch_size=8 \
    --overwrite_output_dir \
    --save_steps 10000 \
    --save_total_limit 2
    
