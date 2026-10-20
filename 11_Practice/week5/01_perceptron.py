"""
Exercise 1: Neuron from Scratch
A single perceptron in pure NumPy, trained on AND and OR (both linearly separable).
"""
import numpy as np


class Perceptron:
    def __init__(self, n_inputs, lr=0.1, epochs=20, seed=0):
        rng = np.random.default_rng(seed)
        self.w = rng.normal(0, 0.1, n_inputs)
        self.b = 0.0
        self.lr = lr
        self.epochs = epochs

    def _predict_one(self, x):
        return int(np.dot(x, self.w) + self.b >= 0)

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

    def fit(self, X, y):
        """Perceptron learning rule: w <- w + lr * (target - prediction) * x."""
        errors_per_epoch = []
        for _ in range(self.epochs):
            errors = 0
            for x, target in zip(X, y):
                update = self.lr * (target - self._predict_one(x))
                self.w += update * x
                self.b += update
                errors += int(update != 0)
            errors_per_epoch.append(errors)
            if errors == 0:          # converged: every sample classified correctly
                break
        return errors_per_epoch


if __name__ == "__main__":
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    gates = {
        "AND": np.array([0, 0, 0, 1]),
        "OR":  np.array([0, 1, 1, 1]),
    }
    for name, y in gates.items():
        p = Perceptron(n_inputs=2, lr=0.1, epochs=50)
        errors = p.fit(X, y)
        preds = p.predict(X)
        print(f"{name}: errors per epoch = {errors}")
        print(f"  weights = {p.w.round(3)}, bias = {round(p.b, 3)}")
        print(f"  predictions = {preds}, targets = {y}, correct = {np.array_equal(preds, y)}\n")
