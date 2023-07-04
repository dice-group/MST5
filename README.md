# Multilingual Knowledge-Based Question Answering

Mengshi Ma's master's thesis

## Generate train data set

lcquad1:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad1/train-data.json \
-o datasets/lcquad1/train.json \
-t lcquad1 \
-l all \
--linguistic_context \
--entity_knowledge 
```

lcquad2:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train.csv \
-t lcquad2 \
-l all \
--linguistic_context \
--entity_knowledge
```

qald dbpedia:
```bash
python3 code/generate_train_csv.py \
-i datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia.json \
-o datasets/qald9plus/dbpedia/qald_9_plus-train_dbpedia.csv \
-t qald \
-kg DBpedia \
-l all \
--linguistic_context \
--entity_knowledge
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
--entity_knowledge
```

## Train on a csv dataset

`train_ds.sh` or `train.sh`

## Evaluation

`eval.sh`

If you only want to export GERBIL results to a csv file:
```bash
python3 code/gerbil_eval.py --experiment_id [experiment_id] --pred_path [path_for_output]
```
