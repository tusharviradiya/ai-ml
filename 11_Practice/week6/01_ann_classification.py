"""
ANN for Classification: Titanic survival prediction (Kaggle).
Download:  kaggle competitions download -c titanic   ->  data/train.csv
Usage:     python 01_ann_classification.py [path/to/train.csv]
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from titanic_prep import split

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"


def eda(df):
    print("Shape:", df.shape)
    print("\nColumn types:\n", df.dtypes)
    print("\nMissing values:\n", df.isna().sum()[lambda s: s > 0])
    print("\nClass balance (Survived):\n", df["Survived"].value_counts(normalize=True).round(3))
    print("\nSurvival rate by Sex:\n", df.groupby("Sex")["Survived"].mean().round(3))
    print("\nSurvival rate by Pclass:\n", df.groupby("Pclass")["Survived"].mean().round(3))

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    df["Age"].hist(bins=30, ax=ax[0]);  ax[0].set_title("Age distribution")
    df["Fare"].clip(upper=200).hist(bins=40, ax=ax[1]); ax[1].set_title("Fare (clipped at 200)")
    df.groupby(["Pclass", "Sex"])["Survived"].mean().unstack().plot.bar(ax=ax[2])
    ax[2].set_title("Survival rate by class and sex")
    plt.tight_layout()
    plt.savefig("01_eda.png", dpi=120)
    plt.close()


if __name__ == "__main__":
    eda(pd.read_csv(PATH))

    (X_tr, y_tr), (X_va, y_va), (X_te, y_te), prep = split(PATH)
    print("\nFeature matrix after encoding and scaling:", X_tr.shape)

    tf.keras.utils.set_random_seed(42)
    model = keras.Sequential([
        keras.Input(shape=(X_tr.shape[1],)),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="binary_crossentropy", metrics=["accuracy"])
    model.summary()

    early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=25, restore_best_weights=True)
    hist = model.fit(X_tr, y_tr, validation_data=(X_va, y_va), epochs=500,
                     batch_size=32, callbacks=[early], verbose=0)
    print(f"\nTraining stopped after {len(hist.history['loss'])} epochs "
          f"(best val_loss at epoch {int(np.argmin(hist.history['val_loss'])) + 1})")

    # Test set is used once, at the very end.
    probs = model.predict(X_te, verbose=0).ravel()
    preds = (probs > 0.5).astype(int)
    print("\n=== Test set results ===")
    print(f"Accuracy: {accuracy_score(y_te, preds):.3f}")
    print(f"F1:       {f1_score(y_te, preds):.3f}")
    print(f"ROC-AUC:  {roc_auc_score(y_te, probs):.3f}")
    print("Confusion matrix [rows=true, cols=pred]:\n", confusion_matrix(y_te, preds))
    print(classification_report(y_te, preds, target_names=["Died", "Survived"]))

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].plot(hist.history["loss"], label="train")
    ax[0].plot(hist.history["val_loss"], label="val")
    ax[0].set_title("Loss"); ax[0].set_xlabel("Epoch"); ax[0].legend()
    ax[1].plot(hist.history["accuracy"], label="train")
    ax[1].plot(hist.history["val_accuracy"], label="val")
    ax[1].set_title("Accuracy"); ax[1].set_xlabel("Epoch"); ax[1].legend()
    plt.tight_layout()
    plt.savefig("01_training_curves.png", dpi=120)
