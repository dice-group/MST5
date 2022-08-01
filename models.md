# Models

## Huggingface Transformers

[Installation](https://huggingface.co/docs/transformers/installation)

## BERT

- encoder based (?)

### mBert

- encoder only (?)

## T5: Text-To-Text Transfer Transformer

https://huggingface.co/docs/transformers/model_doc/t5

### mT5: multilingual pre-trained text-to-text transformer

https://huggingface.co/docs/transformers/model_doc/mt5

pre-trained on mC4, covering 101 languages

pre-trained unsupervisedly -> no real advantage to using a task prefix during single-task fine-tunning

Zero-Shot Generation
- Domain Preserving Training
- Illegal Predictions
  - Normalization: most mT5-XXL illegal predictions are resolved by normalization
  - Grammatical adjustment
  - Accidental translation
    - don't use English only for fine-tuning
    - reduce the language sampling parameter $\alpha$ (e.g. to 0.1)

Q: fine-tune on an English generative task, then it works for all other lanugages?

A: not 100% reliable


# Evaluation

## XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization