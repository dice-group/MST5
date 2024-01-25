#!/bin/bash
#SBATCH -J "mst5-data-prep"
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --gres=gpu:a100:1
#SBATCH --mem 2G
###SBATCH --partition=dgx
###SBATCH --qos=devel
#SBATCH -t 20:00:00
#SBATCH -o "%x_slurm-%j.out"

# Sample usage: sbatch noctua2/noctua2_prepare_data.sh

module load system/CUDA/12.1.0
module load lang/Python/3.11.5-GCCcore-13.2.0

source mst5-venv/bin/activate

# pass the parameters to train script
bash prepare_data.sh "$@" 2>&1