# Week 9: Text Processing, Classical Models, Embeddings, and PyTorch

## Setup
```bash
pip install numpy pandas scikit-learn nltk gensim matplotlib torch kaggle
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```
Exercises 1 and 3 use gensim; exercise 3 can optionally load pretrained GloVe with `--glove`.

### Dataset (exercises 1, 2, 3, 5)
```bash
kaggle datasets download -d lakshmi25npathi/imdb-dataset-of-50k-movie-reviews -p data --unzip
```
The CSV has columns `review` and `sentiment` (positive/negative). If the filename differs, pass it as the first argument.

### Dataset (exercise 4)
Uses the Titanic `train.csv` from week 6. Save it as `data/titanic_train.csv`.

## Files
| File | Purpose |
|---|---|
| `text_pipeline.py` | Shared cleaning, tokenization, stopwords (negations kept), `TextCleaner` sklearn transformer, `load_imdb` split |
| `01_preprocessing_pipeline.py` | Step-by-step cleaning, stemming vs lemmatization comparison |
| `02_classical_text_classification.py` | BoW and TF-IDF × LogReg, Naive Bayes, Linear SVM. Writes `02_results.json`. |
| `03_word_embeddings.py` | Word2Vec (or GloVe), neighbors, analogies, PCA and t-SNE plots |
| `04_pytorch_tabular_ann.py` | Week-6 Titanic ANN in PyTorch: Dataset, DataLoader, manual loop |
| `05_pytorch_lstm_gru_classifier.py` | Embedding + LSTM/GRU in PyTorch, compared with the TF-IDF baseline |

Run order: 02 before 05, because 05 reads the baseline results.

## Design decisions
- **One cleaning function everywhere.** `TextCleaner` is used by all text exercises, so each
  comparison isolates the thing being tested (features, model, or architecture).
- **Negations are kept as stopwords-removed exceptions.** Removing "not" from "not good" flips the label.
- **Stemming vs lemmatization.** Stemming is fast and crude ("movies" → "movi"). Lemmatization gives real
  words but needs a POS to be accurate. The default here assumes nouns, which is a known limitation.
- **Same split for all text models.** `load_imdb` is seeded and stratified, so TF-IDF and the RNN are
  scored on identical test reviews.
- **Validation split from training only** in exercise 5 for early stopping.
- **Gradient clipping** in the RNN loop, which guards against exploding gradients.
- **Packed sequences** in exercise 5, so padding isn't processed by the RNN.
- **Logits + BCEWithLogitsLoss** in PyTorch, which is more numerically stable than sigmoid + BCELoss.

## Results
Fill in after running.

### Exercise 1: Preprocessing
- Vocabulary size (raw, stem, lemma):
- Words where stemming and lemmatization disagree that matter for sentiment, if any:
- Speed difference:

### Exercise 2: Classical models (accuracy / F1 / ROC-AUC)
| Features | Model | Acc | F1 | AUC |
|---|---|---|---|---|
| BoW | LogReg | | | |
| BoW | NB | | | |
| BoW | SVM | | | |
| TF-IDF | LogReg | | | |
| TF-IDF | NB | | | |
| TF-IDF | SVM | | | |

- Which features helped more, BoW or TF-IDF? Which classifier was best, and by how much?
- Words the TF-IDF LogReg relies on most. Do they make sense?

### Exercise 3: Embeddings
- Analogies that worked, and ones that failed. Compare Word2Vec on reviews with GloVe if you ran `--glove`.
- In the 2D plot, do sentiment words cluster together?

### Exercise 4: PyTorch vs Keras (Titanic)
- PyTorch test accuracy / F1 / AUC:
- Keras test accuracy / F1 / AUC from week 6:
- Difference, and whether it's larger than what you'd expect from different initialization.

### Exercise 5: Embeddings + LSTM/GRU
- Test accuracy, F1, AUC for LSTM and GRU, compared with the TF-IDF baseline:
- Did the sequence model beat TF-IDF? Why might a bag of 1-2-grams already be strong on sentiment?
- Training time per epoch and parameter count:
- Run with `gru` as the second argument and compare.
