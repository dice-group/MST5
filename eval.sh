#!/bin/bash

model="mt5-base-qald9-dbpedia"
pred_path=pred_files/${model}


languages=("en" "de" "ru" "fr" "lt" "ba" "be" "uk")


for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/pred_and_build_qald.py \
        --model fine-tuned_models/mt5-base-qald9-dbpedia/checkpoint-20000 \
        -t datasets/qald9plus/dbpedia/qald_9_plus_test_dbpedia.json \
        -o ${pred_path}/${lang}.json \
        -l ${lang}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --exp_setting ${model} \
    --pred_path ${pred_path}


