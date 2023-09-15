#!/bin/bash
# create directories
mkdir -p datasets/lcquad1
mkdir -p datasets/lcquad2
mkdir -p datasets/qald10
# Download lcquad
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/train-data.json datasets/lcquad1/
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/test-data.json datasets/lcquad1/

wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD2.0/master/dataset/train.json datasets/lcquad2/
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD2.0/master/dataset/test.json datasets/lcquad2/
# Download qald10
wget https://raw.githubusercontent.com/KGQA/QALD_10/main/data/qald_10/qald_10.json -P datasets/qald10/