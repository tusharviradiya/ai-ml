"""
Exercise 4: First Keras Model
Rebuilds the 2-4-1 XOR network from Exercise 2 in Keras and compares results.
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y = np.array([[0], [1], [1], [0]], dtype=np.float32)

tf.random.set_seed(1)
model = keras.Sequential([
    keras.Input(shape=(2,)),
    keras.layers.Dense(4, activation="sigmoid"),
    keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=0.5),   # same optimizer as Exercise 2
    loss="binary_crossentropy",
)

# batch_size=len(X) makes each epoch one full-batch step, matching the NumPy version.
history = model.fit(X, y, epochs=10_000, batch_size=len(X), verbose=0)

probs = model.predict(X, verbose=0)
print("Final predictions:")
for xi, yi, pi in zip(X, y, probs):
    print(f"  input={xi.astype(int)}  target={int(yi[0])}  prob={pi[0]:.3f}")
print(f"Final loss: {history.history['loss'][-1]:.4f}")
print(f"Accuracy:   {np.mean((probs > 0.5) == y):.2f}")
print(f"Trainable parameters: {model.count_params()}")
# Compare with 02_neural_net_from_scratch.py: the loss and predictions should be
# similar. Weights won't match exactly because Keras uses Glorot initialization.
