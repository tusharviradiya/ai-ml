"""
Exercise 1: RNN Fundamentals
Task: the label depends ONLY on the first element of a random sequence. Every later
element is noise. The model must carry that one value across T time steps to predict
correctly, so accuracy shows how well each architecture keeps information over long
sequences.

Compares SimpleRNN (vanilla) with LSTM as a reference point across sequence lengths.
"""
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

SEQ_LENGTHS = [10, 25, 50, 100]
N_TRAIN, N_TEST = 5000, 1000
EPOCHS = 15


def make_dataset(n, T, rng):
    X = rng.uniform(-1, 1, size=(n, T, 1)).astype("float32")
    y = (X[:, 0, 0] > 0).astype("float32")          # signal lives in step 0 only
    return X, y


def build(cell, T):
    layer = {"rnn": keras.layers.SimpleRNN, "lstm": keras.layers.LSTM}[cell]
    return keras.Sequential([
        keras.Input(shape=(T, 1)),
        layer(32),
        keras.layers.Dense(1, activation="sigmoid"),
    ])


if __name__ == "__main__":
    results = {"rnn": [], "lstm": []}
    for T in SEQ_LENGTHS:
        rng = np.random.default_rng(T)
        X_tr, y_tr = make_dataset(N_TRAIN, T, rng)
        X_te, y_te = make_dataset(N_TEST, T, rng)
        for cell in results:
            tf.keras.utils.set_random_seed(0)
            model = build(cell, T)
            model.compile(optimizer=keras.optimizers.Adam(1e-3),
                          loss="binary_crossentropy", metrics=["accuracy"])
            model.fit(X_tr, y_tr, validation_split=0.1, epochs=EPOCHS, batch_size=64, verbose=0)
            _, acc = model.evaluate(X_te, y_te, verbose=0)
            results[cell].append(acc)
            print(f"T={T:4d}  {cell:<5}  test accuracy = {acc:.3f}")

    print("\nChance level is 0.500. Accuracy near 0.5 means the model failed to use the first step.")

    plt.figure(figsize=(7, 4.5))
    for cell, accs in results.items():
        plt.plot(SEQ_LENGTHS, accs, marker="o", label=cell.upper())
    plt.axhline(0.5, color="gray", linestyle="--", label="chance")
    plt.xlabel("Sequence length T"); plt.ylabel("Test accuracy")
    plt.title("Long-range memory: SimpleRNN vs LSTM")
    plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
    plt.savefig("01_rnn_vs_lstm_length.png", dpi=120)
    print("Saved 01_rnn_vs_lstm_length.png")
