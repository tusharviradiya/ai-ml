"""
Exercise 2: Neural Net from Scratch
A 2-4-1 feed-forward network in pure NumPy with manual forward and backward
propagation, trained on XOR (not linearly separable, so a hidden layer is required).
"""
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)


class TwoLayerNet:
    def __init__(self, n_in=2, n_hidden=4, lr=0.5, seed=1):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, 1, (n_in, n_hidden))
        self.b1 = np.zeros((1, n_hidden))
        self.W2 = rng.normal(0, 1, (n_hidden, 1))
        self.b2 = np.zeros((1, 1))
        self.lr = lr

    def forward(self, X):
        """Forward pass: cache intermediate values needed for backprop."""
        self.X = X
        self.a1 = sigmoid(X @ self.W1 + self.b1)        # hidden activations
        self.a2 = sigmoid(self.a1 @ self.W2 + self.b2)  # output probability
        return self.a2

    @staticmethod
    def bce_loss(y_hat, y):
        eps = 1e-12
        return -np.mean(y * np.log(y_hat + eps) + (1 - y) * np.log(1 - y_hat + eps))

    def backward(self, y):
        """
        Backward pass (chain rule). With sigmoid output + binary cross-entropy,
        dL/dz2 simplifies to (a2 - y), averaged over N samples.
        """
        N = y.shape[0]
        dz2 = (self.a2 - y) / N
        dW2 = self.a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)

        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.a1 * (1 - self.a1)     # sigmoid'(z) = a(1 - a)
        dW1 = self.X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)
        return dW1, db1, dW2, db2

    def step(self, grads):
        """Vanilla gradient descent update."""
        dW1, db1, dW2, db2 = grads
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2


if __name__ == "__main__":
    net = TwoLayerNet(n_in=2, n_hidden=4, lr=0.5, seed=1)
    losses = []
    for epoch in range(10_000):
        y_hat = net.forward(X)
        losses.append(net.bce_loss(y_hat, y))
        net.step(net.backward(y))

    print("Final predictions:")
    for xi, yi, pi in zip(X, y, net.forward(X)):
        print(f"  input={xi.astype(int)}  target={int(yi[0])}  prob={pi[0]:.3f}")
    print(f"Final accuracy: {np.mean((net.forward(X) > 0.5) == y):.2f}")
    # If accuracy is 0.50 the net got stuck in a poor minimum; try another seed.

    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylabel("Binary cross-entropy")
    plt.title("XOR training loss")
    plt.grid(alpha=0.3)
    plt.savefig("02_loss_curve.png", dpi=120)
    print("Saved 02_loss_curve.png")
