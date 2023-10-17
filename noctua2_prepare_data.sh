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

source mst5-venv/bin/activate

# python3 code/generate_train_csv.py \
# -i datasets/lcquad2/train.json \
# -o datasets/lcquad2/train-lc-ent-noisy.csv \
# -t lcquad2 \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


# python3 code/generate_train_csv.py \
# -i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
# -o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent-noisy.csv \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


# python3 code/generate_train_csv.py \
# -i datasets/qald10/qald10_train.json \
# -o datasets/qald10/qald10_train-lc-ent-noisy.csv \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


python3 code/generate_train_csv.py \
-i datasets/qald10/qald10_train.json \
-o datasets/qald10/qald10_train-lc-ent.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64