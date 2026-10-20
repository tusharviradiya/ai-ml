# Week 10: Pretrained Pipelines, Fine-Tuning BERT, and Baseline Comparison

## Setup
```bash
pip install transformers datasets accelerate torch scikit-learn pandas
```
A GPU is strongly recommended for 02 and 03. DistilBERT on the full IMDB train set takes a
long time on CPU. Google Colab with a GPU runtime works well.

Dataset: the Kaggle IMDB CSV from week 9 (`data/IMDB Dataset.csv`).

## Run order
1. `01_hf_pipelines.py` (downloads four pretrained models on first run)
2. `02_finetune_trainer.py`
3. `03_finetune_pytorch_loop.py`
4. `04_compare_baselines.py`

Script 04 expects the week-9 folder as a sibling directory and reads
`../week-9/05_lstm_results.json` and `../week-9/seq_lstm.pt`. Run week-9 script 05 before
this one. The week-9 version of script 05 has been updated to save `train_time_sec`.

For a quick smoke test, pass a subset size as the second argument to 02 or 03, for example
`python 02_finetune_trainer.py data/IMDB\ Dataset.csv 2000`.

## Files
| File | Purpose |
|---|---|
| `data_utils.py` | Same split as week 9, plus HTML cleanup for transformer input |
| `01_hf_pipelines.py` | Sentiment, NER, QA, and summarization pipelines on chosen probe inputs |
| `02_finetune_trainer.py` | DistilBERT fine-tuning with `Trainer` and full metric reporting |
| `03_finetune_pytorch_loop.py` | The same fine-tuning in a manual loop: AdamW, warmup schedule, clipping, AMP, checkpoint selection |
| `04_compare_baselines.py` | TF-IDF vs LSTM vs DistilBERT on accuracy, F1, AUC, training time, model size |

## Design decisions
- **Identical split everywhere.** `data_utils.load_imdb_split` matches week 9's split exactly, so
  all models are scored on the same reviews.
- **Validation split from training only.** Best epoch is chosen on validation F1, never on test.
- **Dynamic padding** via `DataCollatorWithPadding`, so short reviews don't pay for 256 tokens.
- **Layer-wise weight decay exclusion** (no decay on biases and LayerNorm) in the manual loop, matching
  what `Trainer` does by default.
- **Linear warmup then decay**, and gradient clipping at 1.0. Both are standard for BERT fine-tuning.
- **Raw text for transformers, cleaned text for TF-IDF and LSTM.** Each model gets the input format it
  was designed for. Stopword removal would hurt BERT, which relies on function words.
- **Truncation is a real limitation.** Reviews longer than 256 tokens lose their ending, and sentiment
  often appears late. Note this when you interpret errors.

## Results
Fill in after running.

### Exercise 1: Pipelines
| Task | Model | Succeeded on | Failed on |
|---|---|---|---|
| Sentiment | distilbert-sst2 | | |
| NER | bert-base-NER | | |
| QA | distilbert-squad | | |
| Summarization | distilbart-cnn | | |

- Sentiment: did negation and sarcasm work? What did the mixed-sentiment case return?
- NER: how did lowercase input and the ambiguous "Jordan" case do?
- QA: what did the model answer for "How tall is the Eiffel Tower?" and what score did it return? Why is a low score not enough on its own to detect this failure?
- Summarization: did it drop important content, or invent anything?
- Which failures are about the training domain (SST-2 is movie-like short text), and which are about the task itself?

### Exercise 2: Fine-tuning
- Trainer test metrics (accuracy, precision, recall, F1, AUC):
- Manual-loop test metrics:
- Difference between the two, and whether it's within what you'd expect from randomness:
- Training curves: did validation F1 plateau in epoch 2? Would more epochs have helped?
- Which metric did you pick for best-model selection, and why does F1 make sense here?

### Exercise 3: Baseline vs Transformer
| Model | Accuracy | F1 | ROC-AUC | Train time | Size (MB) |
|---|---|---|---|---|---|
| TF-IDF + LogReg | | | | | |
| PyTorch LSTM | | | | | |
| DistilBERT | | | | | |

- Did DistilBERT beat the baselines, and by how much relative to the seed variation you saw in week 9?
- Was the time and size cost worth the accuracy gain for this task? Put a number on it (accuracy points per hour of training, or per MB).
- Look at the "transformer right, TF-IDF wrong" examples. What do they have in common?
- Which reviews did DistilBERT still get wrong? Were any truncated before the sentiment appeared?
