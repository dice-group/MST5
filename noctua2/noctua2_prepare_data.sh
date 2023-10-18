#!/bin/bash
#SBATCH -J "mst5-data-prep"
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
###SBATCH --gres=gpu:a100:1
#SBATCH --mem 2G
###SBATCH --partition=dgx
###SBATCH --qos=devel
#SBATCH -t 20:00:00
#SBATCH -o "%x_slurm-%j.out"

module load ai/PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load vis/torchvision/0.13.1-foss-2022a-CUDA-11.7.0

source ../mst5-venv/bin/activate

# pass the parameters to train script
cd .. && bash prepare_data.sh "$@"