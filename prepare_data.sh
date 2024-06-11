#!/bin/bash

### To generate training data (simple) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-simple \
-t lcquad2 \
--question_padding_length 128 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-simple \
-t qald \
-kg Wikidata \
-l all \
--question_padding_length 128 \
--train_split_percent 90



### To generate training data (lc) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-lc \
-t lcquad2 \
--linguistic_context \
--question_padding_length 128 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--question_padding_length 128 \
--train_split_percent 90


### To generate training data (ent) ###

python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-ent \
-t lcquad2 \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-ent \
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
-o datasets/lcquad2/train-lc-ent \
-t lcquad2 \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90

## DBpedia based LCQUAD1
# python3 code/generate_train_csv.py \
# -i datasets/lcquad1/train-data.json \
# -o datasets/lcquad1/train-lc-ent \
# -t lcquad1 \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --train_split_percent 90


python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90

## DBpedia based QALD9-Plus
python3 code/generate_train_csv.py \
-i datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia.json \
-o datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia-lc-ent \
-t qald \
-kg DBpedia \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90


### To generate noisy training data (only lc-ent) ###

# python3 code/generate_train_csv.py \
# -i datasets/lcquad2/train.json \
# -o datasets/lcquad2/train-lc-ent-noisy \
# -t lcquad2 \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --extend_with_noisy_entities \
# --train_split_percent 90


# python3 code/generate_train_csv.py \
# -i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
# -o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent-noisy \
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
# -o datasets/qald10/qald10_train-lc-ent-noisy \
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
# -o datasets/qald10/qald10_train-lc-ent \
# -t qald \
# -kg Wikidata \
# -l all \
# --linguistic_context \
# --entity_knowledge \
# --question_padding_length 128 \
# --entity_padding_length 64 \
# --train_split_percent 90

echo "Finished preparing data."