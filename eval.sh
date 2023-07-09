#!/bin/bash

model="exp13-mt5xl-lcquad-lc-ek-pad-dbp-endefr"
pred_path=pred_files/${model}
test_dataset="datasets/qald9plus/dbpedia/qald_9_plus_test_dbpedia-new.json"
knowledge_graph="DBpedia"
languages=("en" "de" "fr")

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
        ${entity_knowledge}
done

echo "Start running GERBIL experiment"
python code/gerbil_eval.py \
    --ref_file_path ${test_dataset} \
    --exp_setting ${model} \
    --pred_path ${pred_path}


