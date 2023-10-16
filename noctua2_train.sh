#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem 200G
#SBATCH -o "train_logs/%x_slurm-%j.out"
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user nikit.srivastava@uni-paderborn.de

module load lib/NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load ai/PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load vis/torchvision/0.13.1-foss-2022a-CUDA-11.7.0

source mst5-venv/bin/activate

export HF_DATASETS_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"
export HUGGINGFACE_HUB_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"
export WANDB_PROJECT="MST5"

PORT=$1
MODEL_NAME=$2
TRAIN_FILE=$3
OUTPUT_DIR=$4
RUN_NAME=$5
TRAIN_EPOCHS=$6
SAVE_STEPS=$7



deepspeed --include=localhost:0 --master_port $PORT code/train_new.py \
    --deepspeed deepspeed/ds_config_zero2.json \
    --model_name_or_path $MODEL_NAME \
    --do_train \
    --train_file $TRAIN_FILE \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs $TRAIN_EPOCHS \
    --per_device_train_batch_size=16 \
    --overwrite_output_dir \
    --save_steps $SAVE_STEPS \
    --save_total_limit 1 \
    --report_to wandb \
    --run_name $RUN_NAME \
    --logging_steps 10 \
    --tf32 1 \
    --fp16 0 \
    --gradient_checkpointing 1 \
    --gradient_accumulation_steps 4