"""
Exercise 2: Real-World Image Classification
CNN with data augmentation on a Kaggle image dataset, followed by an error analysis.
Default dataset: Intel Image Classification (6 scene classes, 150x150 images).
  kaggle datasets download -d puneet6060/intel-image-classification -p data --unzip
  Then arrange as data/train/<class>/ and data/test/<class>/ (see README).
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import confusion_matrix, classification_report
from image_data import load_datasets, augmentation, optimize

tf.keras.utils.set_random_seed(42)


def build_cnn(num_classes, input_shape=(150, 150, 3)):
    inputs = keras.Input(shape=input_shape)
    x = augmentation()(inputs)                      # active only during training
    x = keras.layers.Rescaling(1 / 255)(x)
    for filters in (32, 64, 128, 128):
        x = keras.layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Activation("relu")(x)
        x = keras.layers.MaxPooling2D()(x)
    x = keras.layers.GlobalAveragePooling2D()(x)    # fewer parameters than Flatten
    x = keras.layers.Dropout(0.4)(x)
    outputs = keras.layers.Dense(num_classes, activation="softmax")(x)
    return keras.Model(inputs, outputs)


if __name__ == "__main__":
    train_ds, val_ds, test_ds, classes = load_datasets("data")
    print("Classes:", classes)
    train_ds, val_ds, test_ds = optimize(train_ds), optimize(val_ds), optimize(test_ds)

    model = build_cnn(len(classes))
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3),
    ]
    hist = model.fit(train_ds, validation_data=val_ds, epochs=40, callbacks=callbacks, verbose=2)

    test_loss, test_acc = model.evaluate(test_ds, verbose=0)
    print(f"\nTest accuracy: {test_acc:.3f}")
    model.save("cnn_scratch.keras")
    with open("cnn_scratch_results.json", "w") as f:
        json.dump({"test_accuracy": float(test_acc), "test_loss": float(test_loss),
                   "trainable_params": int(model.count_params())}, f, indent=2)

    # ---- Error analysis ----
    y_true, y_pred, y_conf, errors = [], [], [], []
    for xb, yb in test_ds:
        probs = model.predict(xb, verbose=0)
        pred, conf, true = probs.argmax(1), probs.max(1), yb.numpy()
        y_true += true.tolist(); y_pred += pred.tolist(); y_conf += conf.tolist()
        for i in np.where(pred != true)[0]:
            errors.append((xb[i].numpy().astype("uint8"), true[i], pred[i], conf[i]))

    print("\n" + classification_report(y_true, y_pred, target_names=classes, digits=3))
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion matrix:\n", cm)

    # Most common confusions (off-diagonal, sorted)
    pairs = [(cm[i, j], classes[i], classes[j]) for i in range(len(classes))
             for j in range(len(classes)) if i != j and cm[i, j] > 0]
    print("\nTop confusions (count, true -> predicted):")
    for n, t, p in sorted(pairs, reverse=True)[:5]:
        print(f"  {n:4d}  {t} -> {p}")

    # Confidence of errors: high-confidence mistakes often reveal label noise or ambiguous images.
    confs = np.array([e[3] for e in errors])
    print(f"\nMisclassified: {len(errors)} / {len(y_true)}; "
          f"mean confidence on errors = {confs.mean():.3f}" if len(errors) else "\nNo errors")

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(classes)), classes, rotation=45, ha="right")
    ax.set_yticks(range(len(classes)), classes)
    for i in range(len(classes)):
        for j in range(len(classes)):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=8)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title("Confusion matrix (test)")
    plt.tight_layout(); plt.savefig("02_confusion_matrix.png", dpi=120); plt.close()

    # Grid of the most confident mistakes
    worst = sorted(errors, key=lambda e: -e[3])[:12]
    if worst:
        fig, axes = plt.subplots(3, 4, figsize=(12, 10))
        for a, (img, t, p, c) in zip(axes.ravel(), worst):
            a.imshow(img); a.axis("off")
            a.set_title(f"true: {classes[t]}\npred: {classes[p]} ({c:.2f})", fontsize=9)
        plt.tight_layout(); plt.savefig("02_worst_errors.png", dpi=120); plt.close()

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].plot(hist.history["loss"], label="train"); ax[0].plot(hist.history["val_loss"], label="val")
    ax[0].set_title("Loss"); ax[0].legend()
    ax[1].plot(hist.history["accuracy"], label="train"); ax[1].plot(hist.history["val_accuracy"], label="val")
    ax[1].set_title("Accuracy"); ax[1].legend()
    plt.tight_layout(); plt.savefig("02_training_curves.png", dpi=120); plt.close()
    print("Saved cnn_scratch.keras, cnn_scratch_results.json, and plots.")
