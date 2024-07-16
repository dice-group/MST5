# MST5 — Transformers-based Approach to SPARQL Generation from Multilingual Natural Language Question

Paper: https://arxiv.org/pdf/2407.06041

## Prerequisite

Follow installation instructions in [notebooks/installation_instruction.ipynb](notebooks/installation_instruction.ipynb)

## Generate train & dev data set

lcquad1:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad1/train-data.json \
-o datasets/lcquad1/train-data \
-t lcquad1 \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90
```

lcquad2:
```bash
python3 code/generate_train_csv.py \
-i datasets/lcquad2/train.json \
-o datasets/lcquad2/train-lc-ent \
-t lcquad2 \
-l all \
--linguistic_context \
--entity_knowledge \
--question_padding_length 128 \
--entity_padding_length 64 \
--train_split_percent 90
```

qald dbpedia:
```bash
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
```

qald wikidata:
```bash
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
```

Note: The dev dataset is made noisy by default and is meant only for evaluating the loss. For evaluating the QA system, please look here [Evaluation](#Evaluation)

## Train on a csv dataset

`train.sh` is used to train with DeepSpeed (by default it uses `deepspeed/ds_config_zero2.json`, if you face CUDA out-of-memory issue, try reducing batch-size and/or switching to `deepspeed/ds_config_zero3.json`)

**Note**: THe gradient accumulation is set to 4, which means that for each step the model sees 4x provided batch size.


Please provide arguments in the following order to the training script:
1. PORT : Port to be used by deepspeed
2. MODEL_NAME : Name of the model to fine-tune
3. TRAIN_FILE : Path to the training file
4. EVAL_FILE : Path to the eval file (provide "false" to disable eval logic)
5. OUTPUT_DIR : Output directory to save the fine-tuned model (and checkpoints)
6. RUN_NAME: Name of the run to be used for wandb
7. TRAIN_EPOCHS : Number of epochs to train
8. BATCH_SIZE : Batch size per device
9. SAVE_STEPS: Interval in training steps to save the model checkpoints

Following are sample usages of the training scripts:

#### Fine-tuning on LcQUAD1
```bash
bash train.sh 60020 "google/mt5-xl" datasets/lcquad1/train-data_train_90pct.csv datasets/lcquad1/train-data_dev_10pct.csv fine-tuned_models/lcquad1-finetune_mt5-base_lc-ent lcquad1-finetune_mt5-base_lc-ent 32 32 1000
```
#### Fine-tuning the previous model further on QALD9Plus (DBpedia)
```bash
bash train.sh 60030 fine-tuned_models/lcquad1-finetune_mt5-base_lc-ent datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia-lc-ent_train_90pct.csv datasets/qald9plus/dbpedia/qald_9_plus_train_dbpedia-lc-ent_dev_10pct.csv fine-tuned_models/qald9plus-finetune_lcquad1-ft-base_lc-ent qald9plus-finetune_lcquad1-ft-base_lc-ent 32 32 1000
```

#### Fine-tuning on LcQUAD2
```bash
bash train.sh 60000 "google/mt5-xl" datasets/lcquad2/train-lc-ent_train_90pct.csv datasets/lcquad2/train-lc-ent_dev_10pct.csv fine-tuned_models/lcquad2-finetune_mt5-base_lc-ent lcquad2-finetune_mt5-base_lc-ent 15 32 1000
```
#### Fine-tuning the previous model further on QALD9Plus (Wikidata)
```bash
bash train.sh 60010 fine-tuned_models/lcquad2-finetune_mt5-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent_train_90pct.csv datasets/qald9plus/wikidata/qald_9_plus_train_wikidata-lc-ent_dev_10pct.csv fine-tuned_models/qald9plus-finetune_lcquad2-ft-base_lc-ent qald9plus-finetune_lcquad2-ft-base_lc-ent 32 32 1000
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
8. GE: Gerbil Evaluation : true/false
9. KNOWLEDGE_GRAPH: Knowledge Graph : DBpedia/Wikidata

Sample usage:

```bash
bash eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test "en,de,ru,zh" true true true Wikidata
```
## Fine-tuned Models

You can download the following fine-tuned models that can be used out-of-the-box with the deployment script:

- Wikidata-based model trained on [LC-QuAD2.0](https://github.com/AskNowQA/LC-QuAD2.0) and [Qald_9_Plus](https://github.com/KGQA/QALD_9_plus) (train & test):
```bash
 wget -r -nH --cut-dirs=3 --no-parent --reject="index.html*" https://files.dice-research.org/projects/MST5/fine-tuned-models/qald9plus-finetune_lcquad2-ft-base_lc-ent_testeval/
```
- Wikidata-based model trained on [LC-QuAD2.0](https://github.com/AskNowQA/LC-QuAD2.0) and [Qald_9_Plus](https://github.com/KGQA/QALD_9_plus) (train):
```bash
 wget -r -nH --cut-dirs=3 --no-parent --reject="index.html*" https://files.dice-research.org/projects/MST5/fine-tuned-models/qald9plus-finetune_lcquad2-ft-base_lc-ent/
```
- DBpedia-based model trained on [LC-QuAD1.0](https://github.com/AskNowQA/LC-QuAD) and [Qald_9_Plus](https://github.com/KGQA/QALD_9_plus) (train):
```bash
 wget -r -nH --cut-dirs=3 --no-parent --reject="index.html*" https://files.dice-research.org/projects/MST5/fine-tuned-models/qald9plus-finetune_lcquad1-ft-base_lc-ent/
```

## Model Deployment

To deploy the model as a RESTful service, [deploy_model.py](deploy_model.py) can be used:

```bash
python deploy_model.py --model fine-tuned_models/qald9plus-finetune_lcquad2-ft-base_lc-ent \
    --knowledge_graph Wikidata \
    --linguistic_context \
    --entity_knowledge \
    --question_padding_length 128 \
    --entity_padding_length 64 \
    --port 8181 \
    --log_file logs/server-mst5-wiki.log
```

**Note**: For GPU-based hardware acceleration, set the relevant device in [Text_Generator.py](code/components/Text_Generator.py). To enable CPU-only mode, set the `device` value `-1`.

## Citation
If you use this code or data in your research, please cite our work:
```bibtex
@misc{srivastava2024mst5,
      title={MST5 -- Multilingual Question Answering over Knowledge Graphs}, 
      author={Nikit Srivastava and Mengshi Ma and Daniel Vollmers and Hamada Zahera and Diego Moussallem and Axel-Cyrille Ngonga Ngomo},
      year={2024},
      eprint={2407.06041},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.06041}, 
}
```
