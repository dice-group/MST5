#!/bin/bash

### To generate training data (simple) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-simple.csv \
-t lcquad2 \
--question_padding_length 128 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-simple.csv \
-t qald \
-kg Wikidata \
-l all \
--question_padding_length 128 \
--train_split_percent 90



### To generate training data (lc) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-lc-ent.csv \
-t lcquad2 \
--linguistic_context \
--question_padding_length 128 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--question_padding_length 128 \
--train_split_percent 90


### To generate training data (ent) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-ent.csv \
-t lcquad2 \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-ent.csv \
-t qald \
-kg Wikidata \
-l all \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


### To generate training data (lc-ent) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-lc-ent.csv \
-t lcquad2 \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


### To generate noisy training data (only lc-ent) ###

# python3 code/generate_train_csv.py \
# -i datasets/lcquad2/train.json \
# -o datasets/lcquad2/train-lc-ent-noisy.csv \
# -t lcquad2 \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities \
# --train_split_percent 90


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
# --extend_with_noisy_entities \
# --train_split_percent 90


### To generate QALD10 training data (requires qald10_train.json) (only lc-ent) ###

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
# --extend_with_noisy_entities \
# --train_split_percent 90


# python3 code/generate_train_csv.py \
# -i datasets/qald10/qald10_train.json \
# -o datasets/qald10/qald10_train-lc-ent.csv \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --train_split_percent 90