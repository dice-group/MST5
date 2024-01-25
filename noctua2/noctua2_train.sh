#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:a100:1
#SBATCH --mem 200G
#SBATCH -o "train_logs/%x_slurm-%j.out"
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user nikit.srivastava@uni-paderborn.de

module load system/CUDA/11.8.0
module load lang/Python/3.10.4-GCCcore-11.3.0

source mst5-venv/bin/activate

export WANDB_PROJECT="MST5"

# pass the parameters to train script
bash train.sh "$@"