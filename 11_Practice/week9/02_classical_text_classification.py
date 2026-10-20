"""
Exercise 2: Classical Text Classification
Bag-of-Words and TF-IDF features, each with Logistic Regression, Multinomial Naive Bayes,
and a Linear SVM, on Kaggle IMDB reviews (binary sentiment).

Writes 02_results.json, which exercise 5 reads as its baseline.
Usage: python 02_classical_text_classification.py data/IMDB\ Dataset.csv
"""
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
from text_pipeline import TextCleaner, load_imdb

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"

VECTORIZERS = {
    "BoW": lambda: CountVectorizer(ngram_range=(1, 2), min_df=2, max_features=100_000),
    "TF-IDF": lambda: TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=100_000, sublinear_tf=True),
}
CLASSIFIERS = {
    "LogisticRegression": lambda: LogisticRegression(max_iter=2000, C=2.0),
    "NaiveBayes": lambda: MultinomialNB(alpha=1.0),
    "LinearSVM": lambda: LinearSVC(C=0.5),
}


def scores(pipe, X):
    """Continuous scores for ROC-AUC: decision function where available, else P(positive)."""
    if hasattr(pipe, "decision_function"):
        return pipe.decision_function(X)
    return pipe.predict_proba(X)[:, 1]


if __name__ == "__main__":
    X_tr_raw, X_te_raw, y_tr, y_te = load_imdb(PATH)
    print(f"Train: {len(y_tr)}  Test: {len(y_te)}  Positive rate: {y_tr.mean():.3f}")

    # Cleaning is identical for every model, so do it once (with a fitted-free transformer).
    cleaner = TextCleaner(remove_stopwords=True, normalize=None)
    X_tr, X_te = cleaner.transform(X_tr_raw), cleaner.transform(X_te_raw)

    rows, fitted = [], {}
    for vec_name, make_vec in VECTORIZERS.items():
        for clf_name, make_clf in CLASSIFIERS.items():
            pipe = Pipeline([("vec", make_vec()), ("clf", make_clf())])
            pipe.fit(X_tr, y_tr)
            pred = pipe.predict(X_te)
            row = {
                "features": vec_name, "classifier": clf_name,
                "accuracy": accuracy_score(y_te, pred),
                "f1": f1_score(y_te, pred),
                "roc_auc": roc_auc_score(y_te, scores(pipe, X_te)),
                "n_features": len(pipe.named_steps["vec"].vocabulary_),
            }
            rows.append(row)
            fitted[(vec_name, clf_name)] = (pipe, pred)
            print(f"{vec_name:<7} {clf_name:<20} acc={row['accuracy']:.4f}  "
                  f"f1={row['f1']:.4f}  auc={row['roc_auc']:.4f}  features={row['n_features']}")

    results = pd.DataFrame(rows).round(4)
    print("\n", results.to_string(index=False))
    results.to_csv("02_results.csv", index=False)

    best = results.sort_values("accuracy", ascending=False).iloc[0]
    with open("02_results.json", "w") as f:
        json.dump({"rows": rows, "best": best.to_dict()}, f, indent=2, default=float)

    # Interpretability: the strongest words for each sentiment from TF-IDF + Logistic Regression.
    pipe, _ = fitted[("TF-IDF", "LogisticRegression")]
    names = np.array(pipe.named_steps["vec"].get_feature_names_out())
    coef = pipe.named_steps["clf"].coef_[0]
    order = np.argsort(coef)
    print("\nMost negative words:", list(names[order[:20]]))
    print("Most positive words:", list(names[order[-20:]][::-1]))

    # Error analysis for the best model.
    pipe, pred = fitted[(best["features"], best["classifier"])]
    cm = confusion_matrix(y_te, pred)
    print(f"\nBest model: {best['features']} + {best['classifier']}")
    print("Confusion matrix [rows=true neg/pos, cols=pred neg/pos]:\n", cm)

    fig, ax = plt.subplots(figsize=(10, 4))
    pivot = results.pivot(index="classifier", columns="features", values="accuracy")
    pivot.plot.bar(ax=ax, rot=0)
    ax.set_ylim(0.8, 0.95); ax.set_ylabel("Test accuracy")
    ax.set_title("BoW vs TF-IDF by classifier"); ax.grid(axis="y", alpha=0.3)
    plt.tight_layout(); plt.savefig("02_comparison.png", dpi=120)
    print("Saved 02_results.csv, 02_results.json, 02_comparison.png")
