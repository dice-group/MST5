#!/bin/bash

model="qald9-plus-all"
exp_setting="LC-QuAD-all_lang"
pred_pfad=pred_files/${model}/
linguitic_context="false"
steps=900


languages=("en" "de" "ru" "fr" "zh" "lt" "ja" "ba" "be" "uk")


for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/test_and_build_qald.py \
        --model fine-tuned_models/${model}/checkpoint-${steps} \
        -t datasets/qald9plus/qald_9_pp_test_wikidata_linguistic.json \
        -o pred_files/${model}-${steps}/${lang}.json \
        -l ${lang}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --exp_setting ${exp_setting} \
    --pred_pfad ${pred_pfad}


