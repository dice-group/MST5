# MST5 — Transformers-based Approach to SPARQL Generation from Multilingual Natural Language Question

## Prerequisite

`pip install -r requirements.txt`

<!-- install huggingface from source? -->

## Generate train data set

lcquad1:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad1/train-data.json \
-o datasets/lcquad1/train-data.csv \
-t lcquad1 \
-l all \
--linguistic_context \
--question_padding_length 32 \
--entity_padding_length 5
```

lcquad2:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train.csv \
-t lcquad2 \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 32 \
--entity_padding_length 5
```

qald dbpedia:
```bash
python3 code/generate_train_csv.py \
-i datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia.json \
-o datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia.csv \
-t qald \
-kg DBpedia \
-l all \
--linguistic_context \
--question_padding_length 32 \
--entity_padding_length 5
```

qald wikidata:
```bash
python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 32 \
--entity_padding_length 5
```

## Train on a csv dataset

`train_ds.sh` is used to train with DeepSpeed.

`train.sh` is used to train without DeepSpeed.


- run_name: run name that is showed in wandb
- model_name: name of the base model to be fine-tuned
- output_dir: the output directory of the fine-tuned model, by default is "fine-tuned_models/${run_name}"
- train_file: the path of dataset used in training


## Evaluation

`eval.sh`

If you only want to export GERBIL results to a csv file:
```bash
python3 code/gerbil_eval.py --experiment_id [experiment_id] --pred_path [path_for_output]
```
