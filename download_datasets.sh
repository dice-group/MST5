#!/bin/bash
# create directories
mkdir -p datasets/lcquad1
mkdir -p datasets/lcquad2
mkdir -p datasets/qald10
# Download lcquad
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/train-data.json -P datasets/lcquad1/
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/test-data.json -P datasets/lcquad1/

wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD2.0/master/dataset/train.json -P datasets/lcquad2/
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD2.0/master/dataset/test.json -P datasets/lcquad2/
# Download qald10 
# We use the custom dataset now:
# wget https://raw.githubusercontent.com/KGQA/QALD_10/main/data/qald_10/qald_10.json -P datasets/qald10/