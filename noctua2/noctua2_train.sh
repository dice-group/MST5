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

source ../mst5-venv/bin/activate

export WANDB_PROJECT="MST5"

# pass the parameters to train script
cd .. && bash train.sh "$@"