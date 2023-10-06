# QALD9Plus Dataset

This directory contains the QALD-9-Plus datasets used in the project. 

## Dataset Details

- **Source**: [QALD-9-Plus Repository](https://github.com/KGQA/QALD_9_plus)

## Description

The QALD-9-Plus training datasets are used for fine-tuning after preprocessing in MST5.

The QALD-9-Plus test dataset are used for evaluation and the results can be compared with other systems in KGQA-leaderboard. 

## Update QALD-9-Plus

(For now, don't download the datasets from QALD-9-Plus Github repository, since we have a modified version with Chinese and Japanese translations of the questions. 
A pull request is to be created for QALD-9-Plus Github repository so that the QALD-9-Plus also contains Chinese and Japanese translations.)

In order to track the version of QALD-9-Plus datasets, you can download and update them using

```
wget -N -P datasets/qald9plus/dbpedia https://raw.githubusercontent.com/KGQA/QALD_9_plus/main/data/qald_9_plus_train_dbpedia.json
```
```
wget -N -P datasets/qald9plus/dbpedia https://raw.githubusercontent.com/KGQA/QALD_9_plus/main/data/qald_9_plus_test_dbpedia.json 
```

```
wget -N -P datasets/qald9plus/wikidata https://raw.githubusercontent.com/KGQA/QALD_9_plus/main/data/qald_9_plus_train_wikidata.json
```

```
wget -N -P datasets/qald9plus/wikidata https://raw.githubusercontent.com/KGQA/QALD_9_plus/main/data/qald_9_plus_test_wikidata.json
```

