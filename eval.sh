#!/bin/bash

model="q9pp-ling-context"
exp_setting="all_lang_linguistic_mt5-xl"
pred_pfad=pred_files/${model}/
linguitic_context="True"


languages=("en" "de" "ru" "fr" "zh" "lt" "ja" "ba" "be" "uk")


for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/test_and_build_qald.py \
        --model fine-tuned_models/${model} \
        -t datasets/qald9plus/qald_9_pp_test_wikidata_linguistic.json \
        -o pred_files/${model}/${lang}.json \
        -l ${lang} \
        --linguistic_context ${linguitic_context}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --exp_setting ${exp_setting} \
    --pred_pfad ${pred_pfad}


