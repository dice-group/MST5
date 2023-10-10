#!/bin/bash
#SBATCH -J "MST5 - Training"
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem 220G
###SBATCH --partition=dgx
###SBATCH --qos=devel
#SBATCH -t 40:00:00
#SBATCH -o "train_logs/lcquad2_ft_slurm-%j.out"

# Sample usage: sbatch noctua2_train.sh "lc-ent" 60000

module load lib/NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load ai/PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load vis/torchvision/0.13.1-foss-2022a-CUDA-11.7.0

source mst5-venv/bin/activate

export HF_DATASETS_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"
export HUGGINGFACE_HUB_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"

TRAIN_POSTFIX=$1
PORT=$2

echo Starting training for: $TRAIN_POSTFIX

deepspeed --include=localhost:0 --master_port $PORT code/train_new.py \
    --deepspeed deepspeed/ds_config_zero2.json \
    --model_name_or_path google/mt5-xl \
    --do_train \
    --train_file datasets/lcquad2/train-$TRAIN_POSTFIX.csv \
    --output_dir fine-tuned_models/lcquad2-finetune-$TRAIN_POSTFIX \
    --num_train_epochs 15 \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps 1000 \
    --save_total_limit 2 \
    --report_to wandb \
    --run_name lcquad2-finetune-$TRAIN_POSTFIX \
    --logging_steps 10 \
    --tf32 1 \
    --fp16 0 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4