#!/bin/bash
#SBATCH -J "MST5: dependencies installation"
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:a100:1
#SBATCH -t 01:00:00

# Sample usage: sbatch noctua2/setup_environment.sh .
set -eu

module load system/CUDA/11.8.0
module load lang/Python/3.10.4-GCCcore-11.3.0

# Check if the first argument is set, if not assign the current directory path
MST5_WS=$(pwd)
echo "Current MST5 workspace: ${MST5_WS}"
VENVPATH="${1:-$(pwd)}"
echo "Path to install virtual environment at: ${VENVPATH}"

mkdir -p $VENVPATH

cd $VENVPATH

python -m venv ./mst5-venv

source mst5-venv/bin/activate

#pip3 install --upgrade pip

pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

pip3 install -r requirements.txt

pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download zh_core_web_sm
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
python -m spacy download de_core_news_sm
python -m spacy download ja_core_news_sm
python -m spacy download lt_core_news_sm
python -m spacy download ru_core_news_sm
python -m spacy download es_core_news_sm
python -m spacy download uk_core_news_sm

echo "Dependencies installation finished!"