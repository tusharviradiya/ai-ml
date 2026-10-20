"""
Shared data pipeline for exercises 2 and 3.
Expected layout (one subfolder per class):
    data/train/<class_name>/*.jpg
    data/test/<class_name>/*.jpg
A validation split is carved from train with a fixed seed, so both scripts see identical splits.
"""
from tensorflow import keras

IMG_SIZE = (150, 150)
BATCH = 32
SEED = 42


def load_datasets(data_dir="data", img_size=IMG_SIZE, batch=BATCH):
    train = keras.utils.image_dataset_from_directory(
        f"{data_dir}/train", validation_split=0.2, subset="training", seed=SEED,
        image_size=img_size, batch_size=batch)
    val = keras.utils.image_dataset_from_directory(
        f"{data_dir}/train", validation_split=0.2, subset="validation", seed=SEED,
        image_size=img_size, batch_size=batch)
    test = keras.utils.image_dataset_from_directory(
        f"{data_dir}/test", image_size=img_size, batch_size=batch, shuffle=False)
    class_names = test.class_names
    return train, val, test, class_names


def augmentation():
    """Random transforms applied only during training (Keras disables them at inference)."""
    return keras.Sequential([
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.08),
        keras.layers.RandomZoom(0.1),
        keras.layers.RandomTranslation(0.1, 0.1),
        keras.layers.RandomContrast(0.1),
    ], name="augmentation")


def optimize(ds):
    return ds.cache().prefetch(keras.utils.AUTOTUNE)
