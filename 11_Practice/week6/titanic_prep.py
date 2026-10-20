"""
Shared preprocessing for the Titanic dataset (used by 01 and 03).
Fitting happens on the training split only, so validation and test data
never leak into imputation, scaling, or category levels.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM_COLS = ["Age", "SibSp", "Parch", "Fare", "FamilySize"]
CAT_COLS = ["Pclass", "Sex", "Embarked"]


def load_raw(path):
    df = pd.read_csv(path)
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1   # simple feature engineering
    return df


def make_preprocessor():
    num = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    cat = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer(
        [("num", num, NUM_COLS), ("cat", cat, CAT_COLS)],
        sparse_threshold=0,
    )


def split(path, seed=42):
    """Returns (train, val, test) as (X, y) float32/int arrays, plus the fitted preprocessor."""
    df = load_raw(path)
    X, y = df[NUM_COLS + CAT_COLS], df["Survived"].values
    X_tv, X_te, y_tv, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=seed)
    X_tr, X_va, y_tr, y_va = train_test_split(X_tv, y_tv, test_size=0.2, stratify=y_tv, random_state=seed)

    prep = make_preprocessor().fit(X_tr)              # fit on train only
    transform = lambda A: prep.transform(A).astype("float32")
    return (transform(X_tr), y_tr), (transform(X_va), y_va), (transform(X_te), y_te), prep
