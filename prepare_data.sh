#!/bin/bash

# python3 code/generate_train_csv.py \
# -i datasets/lcquad2/train.json \
# -o datasets/lcquad2/train-lc-ent-noisy.csv \
# -t lcquad2 \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


# python3 code/generate_train_csv.py \
# -i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
# -o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent-noisy.csv \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


# python3 code/generate_train_csv.py \
# -i datasets/qald10/qald10_train.json \
# -o datasets/qald10/qald10_train-lc-ent-noisy.csv \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities


python3 code/generate_train_csv.py \
-i datasets/qald10/qald10_train.json \
-o datasets/qald10/qald10_train-lc-ent.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64