#!/bin/bash

model="mt5/12_mt5"
exp_setting="mt5-base"
pred_path=pred_files/${model}-new/
linguitic_context="True"


languages=("en" "de" "ru" "fr" "zh" "lt" "ja" "ba" "be" "uk")


for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/test_and_build_qald.py \
        --model fine-tuned_models/${model} \
        -t datasets/qald9plus/qald_9_pp_test_wikidata_linguistic.json \
        -o pred_files/${model}/${lang}.json \
        -l ${lang}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --exp_setting ${exp_setting} \
    --pred_path ${pred_path}


