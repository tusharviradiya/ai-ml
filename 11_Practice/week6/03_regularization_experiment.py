"""
Regularization & Tuning Experiment.
One base model (the Titanic ANN from 01) with Dropout, Batch Normalization, and
Early Stopping applied one at a time and then combined.

Each config is run with 3 weight-initialization seeds. The data split is fixed
(seed 42), so the spread reflects training variance, not split variance.
The test set is used once per run for the final numbers.

Usage: python 03_regularization_experiment.py [path/to/train.csv]
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import accuracy_score, roc_auc_score
from titanic_prep import split

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
SEEDS = [0, 1, 2]
MAX_EPOCHS = 300
PATIENCE = 20

CONFIGS = {
    "baseline":   dict(dropout=0.0, bn=False, early_stop=False),
    "dropout":    dict(dropout=0.3, bn=False, early_stop=False),
    "batchnorm":  dict(dropout=0.0, bn=True,  early_stop=False),
    "early_stop": dict(dropout=0.0, bn=False, early_stop=True),
    "all_three":  dict(dropout=0.3, bn=True,  early_stop=True),
}


def build_model(input_dim, dropout, bn):
    model = keras.Sequential([keras.Input(shape=(input_dim,))])
    for units in (64, 32):
        if bn:
            # Dense -> BatchNorm -> activation (BN normalizes before the nonlinearity)
            model.add(keras.layers.Dense(units))
            model.add(keras.layers.BatchNormalization())
            model.add(keras.layers.Activation("relu"))
        else:
            model.add(keras.layers.Dense(units, activation="relu"))
        if dropout > 0:
            model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Dense(1, activation="sigmoid"))
    return model


def run(cfg, seed, data):
    (X_tr, y_tr), (X_va, y_va), (X_te, y_te) = data
    tf.keras.utils.set_random_seed(seed)
    model = build_model(X_tr.shape[1], cfg["dropout"], cfg["bn"])
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="binary_crossentropy", metrics=["accuracy"])

    callbacks = []
    if cfg["early_stop"]:
        callbacks.append(keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=PATIENCE, restore_best_weights=True))

    hist = model.fit(X_tr, y_tr, validation_data=(X_va, y_va), epochs=MAX_EPOCHS,
                     batch_size=32, callbacks=callbacks, verbose=0)

    # Without early stopping, the model is evaluated at its final epoch, which is
    # the realistic outcome of not using early stopping.
    probs = model.predict(X_te, verbose=0).ravel()
    val_loss = np.array(hist.history["val_loss"])
    return {
        "best_val_loss": val_loss.min(),
        "best_epoch": int(val_loss.argmin()) + 1,
        "epochs_run": len(val_loss),
        "final_val_loss": val_loss[-1],
        "gap_val_minus_train": val_loss[-1] - hist.history["loss"][-1],
        "test_acc": accuracy_score(y_te, probs > 0.5),
        "test_auc": roc_auc_score(y_te, probs),
    }, hist.history


if __name__ == "__main__":
    train, val, test, _ = split(PATH)
    data = (train, val, test)

    rows, curves = [], {}
    for name, cfg in CONFIGS.items():
        for seed in SEEDS:
            res, h = run(cfg, seed, data)
            rows.append({"config": name, "seed": seed, **res})
            if seed == SEEDS[0]:
                curves[name] = h
            print(f"{name:<11} seed={seed}  test_acc={res['test_acc']:.3f}  "
                  f"epochs={res['epochs_run']}")

    df = pd.DataFrame(rows)
    df.to_csv("03_all_runs.csv", index=False)

    summary = df.drop(columns="seed").groupby("config", sort=False).agg(["mean", "std"]).round(3)
    print("\n=== Summary (mean over seeds) ===")
    cols = ["best_val_loss", "final_val_loss", "gap_val_minus_train", "test_acc", "test_auc", "epochs_run"]
    print(df.groupby("config", sort=False)[cols].mean().round(3))
    print("\nStd over seeds:")
    print(df.groupby("config", sort=False)[cols].std().round(3))
    summary.to_csv("03_summary.csv")

    fig, ax = plt.subplots(figsize=(8, 5))
    for name, h in curves.items():
        ax.plot(h["val_loss"], label=name)
    ax.set_xlabel("Epoch"); ax.set_ylabel("Validation loss")
    ax.set_title(f"Validation loss by configuration (seed {SEEDS[0]})")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("03_val_loss_comparison.png", dpi=120)
    print("\nSaved 03_all_runs.csv, 03_summary.csv, 03_val_loss_comparison.png")
