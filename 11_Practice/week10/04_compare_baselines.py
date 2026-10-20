"""
Exercise 3: Baseline vs. Transformer
Compares, on the same IMDB test split:
  - TF-IDF + Logistic Regression (re-fit here, timed, same config as week 9)
  - PyTorch LSTM (read from week-9's results; needs week-9's 05 script with train_time_sec)
  - Fine-tuned DistilBERT (from exercise 2's saved model)
on accuracy, F1, ROC-AUC, training time, and model size. Also shows where the transformer
is right and the TF-IDF baseline is wrong.

Usage: python 04_compare_baselines.py data/IMDB\ Dataset.csv
"""
import os
import sys
import json
import time
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from data_utils import load_imdb_split, to_transformer_text

HERE = Path(__file__).resolve().parent
WEEK9 = HERE.parent / "week-9"
sys.path.insert(0, str(WEEK9))
from text_pipeline import TextCleaner   # same cleaning as week 9

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"
TRANSFORMER_DIR = HERE / "distilbert_imdb"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def dir_mb(path):
    return sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(path) for f in fs) / 1e6


def metrics(y, pred, prob):
    return {"accuracy": accuracy_score(y, pred), "f1": f1_score(y, pred),
            "roc_auc": roc_auc_score(y, prob)}


if __name__ == "__main__":
    X_tr_raw, X_te_raw, y_tr, y_te = load_imdb_split(PATH)
    rows = []

    # ---- TF-IDF + LogReg ----
    cleaner = TextCleaner(remove_stopwords=True, normalize=None)
    X_tr, X_te = cleaner.transform(X_tr_raw), cleaner.transform(X_te_raw)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=100_000, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=2.0)),
    ])
    t0 = time.time()
    pipe.fit(X_tr, y_tr)
    tfidf_time = time.time() - t0
    tfidf_prob = pipe.predict_proba(X_te)[:, 1]
    tfidf_pred = (tfidf_prob > 0.5).astype(int)
    tfidf_size = len(pickle.dumps(pipe)) / 1e6
    rows.append({"model": "TF-IDF + LogReg", **metrics(y_te, tfidf_pred, tfidf_prob),
                 "train_time_sec": tfidf_time, "model_size_mb": tfidf_size})

    # ---- LSTM (week 9) ----
    lstm_json = WEEK9 / "05_lstm_results.json"
    lstm_pt = WEEK9 / "seq_lstm.pt"
    if lstm_json.exists():
        with open(lstm_json) as f:
            r = json.load(f)
        rows.append({"model": "PyTorch LSTM", "accuracy": r["accuracy"], "f1": r["f1"],
                     "roc_auc": r["roc_auc"], "train_time_sec": r.get("train_time_sec", np.nan),
                     "model_size_mb": os.path.getsize(lstm_pt) / 1e6 if lstm_pt.exists() else np.nan})
    else:
        print("Week-9 LSTM results not found; skipping the LSTM row.")

    # ---- DistilBERT (exercise 2) ----
    if TRANSFORMER_DIR.exists():
        with open(HERE / "02_trainer_results.json") as f:
            t_train = json.load(f)
        tok = AutoTokenizer.from_pretrained(TRANSFORMER_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(TRANSFORMER_DIR).to(DEVICE).eval()
        probs = []
        texts = to_transformer_text(X_te_raw)
        with torch.no_grad():
            for i in range(0, len(texts), 64):
                enc = tok(texts[i:i + 64], truncation=True, max_length=256,
                          padding=True, return_tensors="pt").to(DEVICE)
                probs.append(torch.softmax(model(**enc).logits, dim=-1)[:, 1].cpu().numpy())
        bert_prob = np.concatenate(probs)
        bert_pred = (bert_prob > 0.5).astype(int)
        rows.append({"model": "DistilBERT (fine-tuned)", **metrics(y_te, bert_pred, bert_prob),
                     "train_time_sec": t_train["train_time_sec"],
                     "model_size_mb": dir_mb(TRANSFORMER_DIR)})

        # Where the transformer wins and the baseline loses.
        wins = np.where((bert_pred == y_te) & (tfidf_pred != y_te))[0][:3]
        print("\nTransformer correct, TF-IDF wrong (examples):")
        for i in wins:
            label = "positive" if y_te[i] else "negative"
            print(f"  true={label}  tfidf_p={tfidf_prob[i]:.2f}  bert_p={bert_prob[i]:.2f}\n"
                  f"  {X_te_raw[i][:200]}...\n")
    else:
        print(f"{TRANSFORMER_DIR} not found. Run 02_finetune_trainer.py first.")

    df = pd.DataFrame(rows)
    pd.set_option("display.width", 140)
    print("=== Comparison on the same test split ===")
    print(df.round(4).to_string(index=False))
    df.to_csv("04_comparison.csv", index=False)
    print("\nSaved 04_comparison.csv")
    print("Note: DistilBERT trained on up to 256 tokens of raw text; the LSTM used 200 tokens of "
          "cleaned text; TF-IDF used all tokens. Training times depend on hardware.")
