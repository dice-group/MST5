#!/bin/bash
set -eu
# model="qald9plus-finetune"
model="lcquad2-pretrain"
# pred_path=pred_files_qald10_new/${model}
pred_path=pred_files_lcquad2qald_new/${model}
# test_dataset="datasets/qald9plus/wikidata/qald_9_plus_test_wikidata_new.json"
# test_dataset="datasets/qald9plus/wikidata/qald_9_plus_test_wikidata_latest.json"
# test_dataset="datasets/qald10/qald_10_latest.json"
test_dataset="datasets/qald_lcquad2/test_qald.json"
knowledge_graph="Wikidata"
question_padding_length=32
entity_padding_length=5
# languages=("en" "de" "ru" "fr" "lt" "ba" "be" "uk" "zh" "ja" "es")
# languages=("en" "de" "ru" "zh")
languages=("en")


include_linguistic_context=true
include_entity_knowledge=true

if [ "$include_linguistic_context" = true ]; then
  linguistic_context="--linguistic_context"
else
  linguistic_context="--no-linguistic_context"
fi

if [ "$include_entity_knowledge" = true ]; then
  entity_knowledge="--entity_knowledge"
else
  entity_knowledge="--no-entity_knowledge"
fi

for lang in "${languages[@]}"
do
    echo "Generating predicted qald file for ${lang}"
    python code/pred_and_build_qald.py \
        --model fine-tuned_models/${model} \
        -t ${test_dataset} \
        --knowledge_graph ${knowledge_graph} \
        -o ${pred_path}/${lang}.json \
        -l ${lang} \
        ${linguistic_context} \
        ${entity_knowledge} \
        --question_padding_length ${question_padding_length} \
        --entity_padding_length ${entity_padding_length}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --ref_file_path ${test_dataset} \
    --exp_setting ${model} \
    --pred_path ${pred_path}


