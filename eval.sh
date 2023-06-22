#!/bin/bash

model="mt5-xl-lcquad-300rt"
pred_path=pred_files/${model}
linguitic_context="True"


languages=("en" "de" "ru" "fr" "zh" "lt" "ja" "ba" "be" "uk")


for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/test_and_build_qald.py \
        --model fine-tuned_models/${model} \
        -t datasets/qald9plus/qald_9_pp_test_wikidata_new.json \
        -o ${pred_path}/${lang}.json \
        -l ${lang} \
        --linguistic_context True \
        --entity_knowledge True
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --exp_setting ${model} \
    --pred_path ${pred_path}


