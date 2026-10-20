"""
Reusable text cleaning and tokenization, shared by exercises 1, 2, 3, and 5.

TextCleaner is a scikit-learn transformer, so it drops into any Pipeline:
    Pipeline([("clean", TextCleaner(normalize="lemma")), ("tfidf", TfidfVectorizer())])
It takes a list of raw documents and returns a list of cleaned, space-joined token strings.
"""
import html
import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
from nltk.stem import PorterStemmer

URL_RE = re.compile(r"https?://\S+|www\.\S+")
HTML_RE = re.compile(r"<[^>]+>")
NON_ALPHA_RE = re.compile(r"[^a-z'\s]")

# Negations carry sentiment. Dropping "not" from "not good" would flip the meaning,
# so they are kept even though sklearn's default stopword list includes them.
NEGATIONS = {"not", "no", "nor", "never", "none", "neither", "without"}
STOP = frozenset(ENGLISH_STOP_WORDS) - NEGATIONS


def clean_text(text):
    """Unescape HTML entities, strip tags and URLs, lowercase, keep letters and apostrophes."""
    text = html.unescape(str(text)).lower()
    text = HTML_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = NON_ALPHA_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(cleaned):
    """Split on whitespace and strip stray apostrophes ("'quoted'" -> "quoted")."""
    return [t for t in (tok.strip("'") for tok in cleaned.split()) if t]


_lemmatizer = None
def get_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        import nltk
        from nltk.stem import WordNetLemmatizer
        for pkg in ("wordnet", "omw-1.4"):
            try:
                nltk.data.find(f"corpora/{pkg}")
            except LookupError:
                nltk.download(pkg, quiet=True)
        _lemmatizer = WordNetLemmatizer()
    return _lemmatizer


class TextCleaner(BaseEstimator, TransformerMixin):
    """
    remove_stopwords: drop common function words (negations are kept).
    normalize: None, "stem" (Porter stemmer), or "lemma" (WordNet lemmatizer, noun POS by default).
    """

    def __init__(self, remove_stopwords=True, normalize=None):
        self.remove_stopwords = remove_stopwords
        self.normalize = normalize

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        stemmer = PorterStemmer() if self.normalize == "stem" else None
        lemmatizer = get_lemmatizer() if self.normalize == "lemma" else None
        out = []
        for doc in X:
            tokens = tokenize(clean_text(doc))
            if self.remove_stopwords:
                tokens = [t for t in tokens if t not in STOP]
            if stemmer is not None:
                tokens = [stemmer.stem(t) for t in tokens]
            elif lemmatizer is not None:
                tokens = [lemmatizer.lemmatize(t) for t in tokens]
            out.append(" ".join(tokens))
        return out


def load_imdb(path, test_size=0.2, seed=42):
    """
    Kaggle IMDB Dataset.csv (columns: review, sentiment). Returns raw train/test arrays.
    The split is stratified and seeded, so every exercise that calls this sees the same test set.
    """
    df = pd.read_csv(path).drop_duplicates(subset="review")
    y = (df["sentiment"].str.lower() == "positive").astype(int).values
    X_tr, X_te, y_tr, y_te = train_test_split(
        df["review"].values, y, test_size=test_size, stratify=y, random_state=seed)
    return X_tr, X_te, y_tr, y_te
