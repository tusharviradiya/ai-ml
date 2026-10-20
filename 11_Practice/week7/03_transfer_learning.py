"""
Exercise 3: Transfer Learning
Fine-tunes an ImageNet-pretrained ResNet50 on the same dataset as exercise 2 and
compares it with the from-scratch CNN (reads cnn_scratch_results.json from 02).

Two phases:
  1. Feature extraction: freeze the base, train only the new classification head.
  2. Fine-tuning: unfreeze the top layers and train with a much smaller learning rate.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from image_data import load_datasets, augmentation, optimize

tf.keras.utils.set_random_seed(42)
UNFREEZE_LAST = 30   # number of top ResNet50 layers to fine-tune in phase 2


def build_transfer_model(num_classes, input_shape=(150, 150, 3)):
    base = keras.applications.ResNet50(include_top=False, weights="imagenet",
                                       input_shape=input_shape)
    base.trainable = False
    inputs = keras.Input(shape=input_shape)
    x = augmentation()(inputs)
    x = base(x, training=False)          # training=False keeps BatchNorm in inference mode
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.3)(x)
    outputs = keras.layers.Dense(num_classes, activation="softmax")(x)
    return keras.Model(inputs, outputs), base


def unfreeze_top(base, n):
    base.trainable = True
    for layer in base.layers[:-n]:
        layer.trainable = False
    # Keep BatchNorm frozen: small batches make its running statistics unstable to update.
    for layer in base.layers:
        if isinstance(layer, keras.layers.BatchNormalization):
            layer.trainable = False


def preprocess(ds):
    # ResNet50 expects its own input normalization, applied to raw 0-255 pixels.
    pp = keras.applications.resnet50.preprocess_input
    return ds.map(lambda x, y: (pp(x), y), num_parallel_calls=tf.data.AUTOTUNE)


if __name__ == "__main__":
    train_ds, val_ds, test_ds, classes = load_datasets("data")
    train_ds = optimize(preprocess(train_ds))
    val_ds = optimize(preprocess(val_ds))
    test_ds = optimize(preprocess(test_ds))

    model, base = build_transfer_model(len(classes))
    loss = "sparse_categorical_crossentropy"

    # ---- Phase 1: train the head only ----
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss=loss, metrics=["accuracy"])
    print("Trainable params (phase 1):", sum(np.prod(v.shape) for v in model.trainable_weights))
    h1 = model.fit(train_ds, validation_data=val_ds, epochs=8, verbose=2)

    # ---- Phase 2: fine-tune the top of the base ----
    unfreeze_top(base, UNFREEZE_LAST)
    model.compile(optimizer=keras.optimizers.Adam(1e-5), loss=loss, metrics=["accuracy"])
    print("Trainable params (phase 2):", sum(np.prod(v.shape) for v in model.trainable_weights))
    callbacks = [keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True)]
    h2 = model.fit(train_ds, validation_data=val_ds, epochs=20, callbacks=callbacks, verbose=2)

    test_loss, test_acc = model.evaluate(test_ds, verbose=0)
    print(f"\nTransfer model test accuracy: {test_acc:.3f}")
    model.save("transfer_resnet50.keras")

    # ---- Comparison with the from-scratch CNN ----
    with open("cnn_scratch_results.json") as f:
        scratch = json.load(f)
    print("\n=== Comparison (same test split) ===")
    print(f"{'model':<22}{'test acc':>10}{'trainable params':>20}")
    print(f"{'scratch CNN':<22}{scratch['test_accuracy']:>10.3f}{scratch['trainable_params']:>20,}")
    print(f"{'ResNet50 fine-tuned':<22}{test_acc:>10.3f}{int(model.count_params()):>20,}")

    val_acc = h1.history["val_accuracy"] + h2.history["val_accuracy"]
    plt.figure(figsize=(8, 4))
    plt.plot(val_acc, label="ResNet50 val accuracy")
    plt.axvline(len(h1.history["val_accuracy"]), color="gray", linestyle="--", label="unfreeze")
    plt.xlabel("Epoch"); plt.ylabel("Validation accuracy"); plt.legend(); plt.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("03_transfer_curves.png", dpi=120)
    print("Saved transfer_resnet50.keras and 03_transfer_curves.png")
