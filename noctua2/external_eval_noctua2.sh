#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=04:00:00
#SBATCH -o "eval_logs/%x_slurm-%j.out"

# Sample usage: sbatch --job-name=external_eval noctua2/external_eval_noctua2.sh deeppavlov2023,qanary datasets/qald10/qald_10.json predictions_external_qald10_test en,ru true Wikidata en
# Sample usage: sbatch --job-name=external_eval noctua2/external_eval_noctua2.sh deeppavlov2023 datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_external_wikidata_qald9plus_test en false Wikidata
set -eu
# Setting up environment
module load lib/NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load ai/PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load vis/torchvision/0.13.1-foss-2022a-CUDA-11.7.0

source mst5-venv/bin/activate

# pass the parameters to train script
bash eval_external.sh "$@"