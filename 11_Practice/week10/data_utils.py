"""
Shared data helpers for week 10. load_imdb_split uses the same split as week-9's
text_pipeline.load_imdb (same dedupe, stratification, and seed), so the TF-IDF, LSTM,
and DistilBERT models are scored on identical test reviews.
"""
import pandas as pd
from sklearn.model_selection import train_test_split

MODEL_NAME = "distilbert-base-uncased"
MAX_LEN = 256   # reviews are long; 256 tokens covers most of the signal and keeps training affordable


def load_imdb_split(path, test_size=0.2, seed=42):
    df = pd.read_csv(path).drop_duplicates(subset="review")
    y = (df["sentiment"].str.lower() == "positive").astype(int).values
    X_tr, X_te, y_tr, y_te = train_test_split(
        df["review"].values, y, test_size=test_size, stratify=y, random_state=seed)
    return X_tr, X_te, y_tr, y_te


def to_transformer_text(texts):
    """Transformers see raw text. Only the HTML line breaks in IMDB are removed."""
    return [t.replace("<br />", " ") for t in texts]
