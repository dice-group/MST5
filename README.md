# MST5 — Transformers-based Approach to SPARQL Generation from Multilingual Natural Language Question

## Prerequisite

Follow installation instructions in [notebooks/installation_instruction.ipynb](notebooks/installation_instruction.ipynb)

## Generate train data set

lcquad1:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad1/train-data.json \
-o datasets/lcquad1/train-data.csv \
-t lcquad1 \
-l all \
--linguistic_context \
--question_padding_length 128 \
--entity_padding_length 64
```

lcquad2:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-lc-ent.csv \
-t lcquad2 \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64
```

qald dbpedia:
```bash
python3 code/generate_train_csv.py \
-i datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia.json \
-o datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia-lc-ent.csv \
-t qald \
-kg DBpedia \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64
```

qald wikidata:
```bash
python3 code/generate_train_csv.py \
-i datasets/qald9plus/wikidata/qald_9_plus_train_wikidata.json \
-o datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent.csv \
-t qald \
-kg Wikidata \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64
```

## Train on a csv dataset

`train.sh` is used to train with DeepSpeed (by default it uses `deepspeed/ds_config_zero2.json`, if you face CUDA out-of-memory issue, try reducing batch-size and/or switching to `deepspeed/ds_config_zero3.json`)


Please provide arguments in the following order to the training script:
1. PORT : Port to be used by deepspeed
2. MODEL_NAME : Name of the model to fine-tune
3. TRAIN_FILE : Path to the training file
4. OUTPUT_DIR : Output directory to save the fine-tuned model (and checkpoints)
5. RUN_NAME: Name of the run to be used for wandb
6. TRAIN_EPOCHS : Number of epochs to train
7. SAVE_STEPS: Interval in training steps to save the model checkpoints

Following are sample usages of the training scripts:

#### Fine-tuning on LcQUAD2
```bash
bash train.sh 60000 "google/mt5-xl" datasets/lcquad2/train-lc-ent.csv fine-tuned_models/lcquad2-finetune_mt5-base_lc-ent lcquad2-finetune_mt5-base_lc-ent 15 1000
```
#### Fine-tuning the previous model further on QALD9Plus (Wikidata)
```bash
bash train.sh 60010 fine-tuned_models/lcquad2-finetune_mt5-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent.csv fine-tuned_models/qald9plus-finetune_lcquad2-ft-base_lc-ent qald9plus-finetune_lcquad2-ft-base_lc-ent 32 1000
```

## Evaluation

Please provide arguments in the following order to the evaluation script:
1. MODEL_ROOT_DIR : Directory where fine-tuned models are stored: fine-tuned_models
2. MODEL_NAME : Name of the model: qald9plus-finetune_mt5-base_lc-ent
3. TEST_FILE : Path to the qald test file
4. OUTPUT_DIR : Root directory where a new directory with model_name will be created to store predictions and results
5. LANGS : Comma separated values e.g: en,de,es
6. LC : linguistic context : true/false
7. EK : entity knowledge : true/false

Sample usage:

```bash
bash eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test "en,de,ru,zh" true true
```
