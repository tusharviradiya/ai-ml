"""
Exercise 1: CNN from Basics
Builds a CNN from scratch on CIFAR-10 (downloaded automatically by Keras),
trains it, and visualizes feature maps from an early and a late layer.
"""
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

CLASSES = ["airplane", "automobile", "bird", "cat", "deer",
           "dog", "frog", "horse", "ship", "truck"]


def conv_block(x, filters):
    """Conv -> BN -> ReLU, twice, then downsample. Stacking blocks builds hierarchical features."""
    for _ in range(2):
        x = keras.layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation("relu")(x)
    return keras.layers.MaxPooling2D()(x)


def build_cnn():
    inputs = keras.Input(shape=(32, 32, 3))
    x = keras.layers.Rescaling(1 / 255)(inputs)     # scale pixels to [0, 1]
    for filters in (32, 64, 128):
        x = conv_block(x, filters)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(128, activation="relu")(x)
    x = keras.layers.Dropout(0.5)(x)
    outputs = keras.layers.Dense(10, activation="softmax")(x)
    return keras.Model(inputs, outputs)


if __name__ == "__main__":
    (x_tr, y_tr), (x_te, y_te) = keras.datasets.cifar10.load_data()
    y_tr, y_te = y_tr.ravel(), y_te.ravel()
    print("Train:", x_tr.shape, "Test:", x_te.shape)

    tf.keras.utils.set_random_seed(0)
    model = build_cnn()
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    hist = model.fit(x_tr, y_tr, validation_split=0.1, epochs=15, batch_size=64, verbose=2)
    test_loss, test_acc = model.evaluate(x_te, y_te, verbose=0)
    print(f"\nTest accuracy: {test_acc:.3f}")
    model.save("cnn_cifar10.keras")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].plot(hist.history["loss"], label="train"); ax[0].plot(hist.history["val_loss"], label="val")
    ax[0].set_title("Loss"); ax[0].legend(); ax[0].set_xlabel("Epoch")
    ax[1].plot(hist.history["accuracy"], label="train"); ax[1].plot(hist.history["val_accuracy"], label="val")
    ax[1].set_title("Accuracy"); ax[1].legend(); ax[1].set_xlabel("Epoch")
    plt.tight_layout(); plt.savefig("01_training_curves.png", dpi=120); plt.close()

    # ---- Feature map visualization ----
    # Use post-ReLU activations: they show which features each filter actually fires on.
    relu_layers = [l for l in model.layers if isinstance(l, keras.layers.Activation)]
    feat_model = keras.Model(model.input, [l.output for l in relu_layers])

    idx = 3
    sample = x_te[idx:idx + 1]
    maps = feat_model.predict(sample, verbose=0)
    show = [0, len(maps) - 1]          # first block (edges, colors) and last block (shapes, parts)

    fig, axes = plt.subplots(3, 8, figsize=(16, 7))
    axes[0, 0].imshow(sample[0].astype("uint8"))
    axes[0, 0].set_title(f"Input: {CLASSES[y_te[idx]]}")
    for a in axes[0, 1:]:
        a.axis("off")
    for row, li in enumerate(show, start=1):
        fm = maps[li][0]
        chans = np.linspace(0, fm.shape[-1] - 1, 8).astype(int)
        for col, c in enumerate(chans):
            axes[row, col].imshow(fm[..., c], cmap="viridis")
            axes[row, col].set_title(f"{relu_layers[li].name} ch{c}", fontsize=7)
            axes[row, col].axis("off")
    plt.tight_layout()
    plt.savefig("01_feature_maps.png", dpi=120)
    print("Saved 01_training_curves.png, 01_feature_maps.png, cnn_cifar10.keras")
