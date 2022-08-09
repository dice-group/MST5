# Models

## Huggingface Transformers

[Installation](https://huggingface.co/docs/transformers/installation)

## Transformer

## BERT

- Bidirectional Encoder Representations from Transformers
- Transformer encoder: bidirectional transformer
- Bidirectioal: each word can see itself indirectly based on left and right context
- training:
  - mask words
  - next sentence prediction

### mBert

- encoder only
- 104 languages
- Zero shot

## T5: Text-To-Text Transfer Transformer

[huggingface t5](https://huggingface.co/docs/transformers/model_doc/t5)

- Encoder-Decoder architecture
- Casual with prefix mask
- Unsupervised objectives
- pre-trained on C4
- allows the use of exactly the same training objective (teacher-forced maximum- likelihood) for every task

### mT5: multilingual pre-trained text-to-text transformer

[huggingface mt5](https://huggingface.co/docs/transformers/model_doc/mt5)

- pre-trained on mC4
- 101 languages
- pre-trained unsupervisedly -> no real advantage to using a task prefix during single-task fine-tunning

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

## XLM

- BERT-based
- cross-lingual pre-training objectives
- 100 languages

### XLM-R

- trained with a cross-lingual masked language modeling objective
- 100 languages

## BART

### mBART

- trained with a combination of span masking and sentence shuffling objectives
- 25 languages (subset of XLM-R)
- denoising full texts in multiple languages

## MARGE

- encoder-decoder
- reconstruct a document in one language by retrieving documents in other languages
- 26 languages

# Evaluation

## XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization