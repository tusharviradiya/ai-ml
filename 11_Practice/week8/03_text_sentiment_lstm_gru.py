"""
Exercise 3: Sequence/Text Modeling
Binary sentiment classification on IMDB movie reviews (downloaded by Keras, no Kaggle needed).
Same architecture with an LSTM and a GRU, each run with 3 seeds, compared on accuracy,
parameter count, and training time.
"""
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.datasets import imdb

VOCAB = 10_000     # keep the 10k most frequent words
MAXLEN = 200       # truncate/pad reviews to this many tokens
EMBED = 64
UNITS = 64
SEEDS = [0, 1, 2]
EPOCHS = 10


def build(cell):
    Cell = {"lstm": keras.layers.LSTM, "gru": keras.layers.GRU}[cell]
    return keras.Sequential([
        keras.Input(shape=(MAXLEN,)),
        # mask_zero=True tells the RNN to skip padding tokens instead of processing them.
        keras.layers.Embedding(VOCAB, EMBED, mask_zero=True),
        Cell(UNITS),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(1, activation="sigmoid"),
    ])


if __name__ == "__main__":
    (x_tr, y_tr), (x_te, y_te) = imdb.load_data(num_words=VOCAB)
    # Pre-padding and pre-truncation keep the most recent tokens next to the RNN's final state,
    # which is what the classifier reads out.
    x_tr = keras.utils.pad_sequences(x_tr, maxlen=MAXLEN, padding="pre", truncating="pre")
    x_te = keras.utils.pad_sequences(x_te, maxlen=MAXLEN, padding="pre", truncating="pre")
    print("Train:", x_tr.shape, "Test:", x_te.shape, "Positive rate:", y_tr.mean().round(3))

    rows, curves = [], {}
    for cell in ["lstm", "gru"]:
        for seed in SEEDS:
            tf.keras.utils.set_random_seed(seed)
            model = build(cell)
            model.compile(optimizer=keras.optimizers.Adam(1e-3),
                          loss="binary_crossentropy", metrics=["accuracy"])
            early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=3,
                                                  restore_best_weights=True)
            t0 = time.time()
            hist = model.fit(x_tr, y_tr, validation_split=0.2, epochs=EPOCHS,
                             batch_size=128, callbacks=[early], verbose=0)
            elapsed = time.time() - t0
            _, test_acc = model.evaluate(x_te, y_te, verbose=0)
            rows.append({
                "cell": cell.upper(), "seed": seed,
                "test_acc": test_acc,
                "best_val_acc": max(hist.history["val_accuracy"]),
                "epochs_run": len(hist.history["loss"]),
                "params": model.count_params(),
                "sec_per_epoch": elapsed / len(hist.history["loss"]),
            })
            if seed == SEEDS[0]:
                curves[cell] = hist.history
            print(f"{cell.upper():<5} seed={seed}  test_acc={test_acc:.4f}  "
                  f"epochs={rows[-1]['epochs_run']}  sec/epoch={rows[-1]['sec_per_epoch']:.1f}")

    df = pd.DataFrame(rows)
    df.to_csv("03_all_runs.csv", index=False)
    cols = ["test_acc", "best_val_acc", "epochs_run", "params", "sec_per_epoch"]
    print("\n=== Mean over seeds ===")
    print(df.groupby("cell")[cols].mean().round(4))
    print("\n=== Std over seeds ===")
    print(df.groupby("cell")[cols].std().round(4))

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    for cell, h in curves.items():
        ax[0].plot(h["val_accuracy"], label=cell.upper())
        ax[1].plot(h["val_loss"], label=cell.upper())
    ax[0].set_title(f"Validation accuracy (seed {SEEDS[0]})"); ax[0].legend()
    ax[1].set_title(f"Validation loss (seed {SEEDS[0]})"); ax[1].legend()
    for a in ax:
        a.set_xlabel("Epoch"); a.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("03_lstm_vs_gru.png", dpi=120)
    print("Saved 03_all_runs.csv and 03_lstm_vs_gru.png")
