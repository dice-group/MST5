#!/bin/bash

model="11_linguistic_mt5"
ling_context="--linguistic_context"


languages=("en" "de" "ru" "fr" "zh" "lt" "ja" "ba" "be" "hy" "uk" "es")

for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python process_functions/test_and_build_qald.py --model fine-tuned_models/${model} -t datasets/qald_9_plus/qald_9_pp_test_wikidata_linguistic.json -o pred_files/${model}/${lang}.json -l ${lang} ${ling_context}
done
