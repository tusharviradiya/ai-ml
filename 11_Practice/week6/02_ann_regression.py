"""
ANN for Regression: Ames house prices (Kaggle "House Prices: Advanced Regression Techniques").
Download:  kaggle competitions download -c house-prices-advanced-regression-techniques
           -> data/house_train.csv
Usage:     python 02_ann_regression.py [path/to/house_train.csv]

Target is log1p(SalePrice), which tames the right skew and matches the Kaggle RMSLE metric.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/house_train.csv"


def eda(df):
    print("Shape:", df.shape)
    print("\nSalePrice summary:\n", df["SalePrice"].describe().round(0))
    print(f"\nSkew raw: {df['SalePrice'].skew():.2f}   skew log1p: {np.log1p(df['SalePrice']).skew():.2f}")
    missing = df.isna().mean().sort_values(ascending=False)
    print("\nTop missing-value columns (fraction):\n", missing[missing > 0].head(8).round(2))
    print("\nColumn types:", df.dtypes.value_counts().to_dict())

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    df["SalePrice"].hist(bins=50, ax=ax[0]); ax[0].set_title("SalePrice (raw)")
    np.log1p(df["SalePrice"]).hist(bins=50, ax=ax[1]); ax[1].set_title("log1p(SalePrice)")
    plt.tight_layout(); plt.savefig("02_eda_target.png", dpi=120); plt.close()


def make_preprocessor(num_cols, cat_cols):
    num = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    cat = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                    ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([("num", num, num_cols), ("cat", cat, cat_cols)], sparse_threshold=0)


if __name__ == "__main__":
    df = pd.read_csv(PATH)
    eda(df)

    # Drop columns that are mostly empty (no reliable signal), plus the ID column.
    df = df.loc[:, df.isna().mean() < 0.4].drop(columns=["Id"])
    y = np.log1p(df.pop("SalePrice")).values
    X = df
    num_cols = X.select_dtypes(include="number").columns.tolist()
    cat_cols = X.select_dtypes(exclude="number").columns.tolist()
    print(f"\n{len(num_cols)} numeric and {len(cat_cols)} categorical features")

    X_tv, X_te, y_tv, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    X_tr, X_va, y_tr, y_va = train_test_split(X_tv, y_tv, test_size=0.2, random_state=42)

    prep = make_preprocessor(num_cols, cat_cols).fit(X_tr)
    X_tr, X_va, X_te = [prep.transform(A).astype("float32") for A in (X_tr, X_va, X_te)]
    print("Encoded feature matrix:", X_tr.shape)

    tf.keras.utils.set_random_seed(42)
    model = keras.Sequential([
        keras.Input(shape=(X_tr.shape[1],)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(1),                       # linear output for regression
    ])
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="mse", metrics=["mae"])

    early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=30, restore_best_weights=True)
    hist = model.fit(X_tr, y_tr, validation_data=(X_va, y_va), epochs=500,
                     batch_size=32, callbacks=[early], verbose=0)
    print(f"Stopped after {len(hist.history['loss'])} epochs")

    # Evaluate on the untouched test set, converting back to dollars.
    pred_log = model.predict(X_te, verbose=0).ravel()
    pred = np.expm1(pred_log)
    actual = np.expm1(y_te)

    baseline = np.full_like(actual, np.expm1(y_tr.mean()))   # always predict the mean price

    def report(name, p):
        rmsle = np.sqrt(mean_squared_error(np.log1p(actual), np.log1p(p)))
        print(f"{name:<12} MAE ${mean_absolute_error(actual, p):>10,.0f}   "
              f"RMSE ${np.sqrt(mean_squared_error(actual, p)):>10,.0f}   "
              f"R2 {r2_score(actual, p):6.3f}   RMSLE {rmsle:.4f}")

    print("\n=== Test set results ===")
    report("Mean baseline", baseline)
    report("ANN", pred)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].scatter(actual, pred, alpha=0.4, s=12)
    lims = [actual.min(), actual.max()]
    ax[0].plot(lims, lims, "r--"); ax[0].set_xlabel("Actual price"); ax[0].set_ylabel("Predicted price")
    ax[0].set_title("Predicted vs actual (test)")
    ax[1].plot(hist.history["loss"], label="train"); ax[1].plot(hist.history["val_loss"], label="val")
    ax[1].set_title("MSE loss (log scale target)"); ax[1].set_xlabel("Epoch"); ax[1].legend()
    plt.tight_layout(); plt.savefig("02_regression_results.png", dpi=120)
