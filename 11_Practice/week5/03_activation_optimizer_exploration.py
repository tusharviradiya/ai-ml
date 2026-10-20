"""
Exercise 3: Activation & Optimizer Exploration
Same 2-H-1 network, same dataset (two concentric circles, not linearly separable),
swept over activation functions and optimizers. Loss curves are plotted for each.
"""
import numpy as np
import matplotlib.pyplot as plt


def make_circles(n=400, seed=0):
    rng = np.random.default_rng(seed)
    n2 = n // 2
    r_in = 0.5 + rng.normal(0, 0.05, n2)
    r_out = 1.0 + rng.normal(0, 0.05, n2)
    t_in = rng.uniform(0, 2 * np.pi, n2)
    t_out = rng.uniform(0, 2 * np.pi, n2)
    X = np.vstack([
        np.c_[r_in * np.cos(t_in), r_in * np.sin(t_in)],
        np.c_[r_out * np.cos(t_out), r_out * np.sin(t_out)],
    ])
    y = np.r_[np.zeros(n2), np.ones(n2)].reshape(-1, 1)
    return X, y


# Each entry: (forward f(z), derivative expressed in terms of the activation output a)
ACTIVATIONS = {
    "sigmoid": (lambda z: 1 / (1 + np.exp(-z)), lambda a: a * (1 - a)),
    "tanh":    (np.tanh,                        lambda a: 1 - a ** 2),
    "relu":    (lambda z: np.maximum(0, z),     lambda a: (a > 0).astype(float)),
}


class SGD:
    def __init__(self, lr):
        self.lr = lr

    def step(self, params, grads):
        for k in params:
            params[k] -= self.lr * grads[k]


class Momentum:
    def __init__(self, lr, beta=0.9):
        self.lr, self.beta, self.v = lr, beta, {}

    def step(self, params, grads):
        for k in params:
            self.v[k] = self.beta * self.v.get(k, 0) - self.lr * grads[k]
            params[k] += self.v[k]


class Adam:
    def __init__(self, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads):
        self.t += 1
        for k in params:
            g = grads[k]
            self.m[k] = self.b1 * self.m.get(k, 0) + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v.get(k, 0) + (1 - self.b2) * g * g
            m_hat = self.m[k] / (1 - self.b1 ** self.t)
            v_hat = self.v[k] / (1 - self.b2 ** self.t)
            params[k] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


class MLP:
    def __init__(self, n_in, n_hidden, activation, seed=0):
        rng = np.random.default_rng(seed)
        self.f, self.df = ACTIVATIONS[activation]
        self.p = {
            "W1": rng.normal(0, 1 / np.sqrt(n_in), (n_in, n_hidden)),
            "b1": np.zeros((1, n_hidden)),
            "W2": rng.normal(0, 1 / np.sqrt(n_hidden), (n_hidden, 1)),
            "b2": np.zeros((1, 1)),
        }

    def forward(self, X):
        self.X = X
        self.a1 = self.f(X @ self.p["W1"] + self.p["b1"])
        self.a2 = 1 / (1 + np.exp(-(self.a1 @ self.p["W2"] + self.p["b2"])))  # sigmoid output
        return self.a2

    def loss(self, y_hat, y):
        eps = 1e-12
        return -np.mean(y * np.log(y_hat + eps) + (1 - y) * np.log(1 - y_hat + eps))

    def backward(self, y):
        N = y.shape[0]
        dz2 = (self.a2 - y) / N
        grads = {"W2": self.a1.T @ dz2, "b2": dz2.sum(axis=0, keepdims=True)}
        dz1 = (dz2 @ self.p["W2"].T) * self.df(self.a1)
        grads["W1"] = self.X.T @ dz1
        grads["b1"] = dz1.sum(axis=0, keepdims=True)
        return grads


def train(activation, optimizer, X, y, epochs=2000, n_hidden=8, seed=0):
    net = MLP(X.shape[1], n_hidden, activation, seed=seed)
    history = []
    for _ in range(epochs):
        y_hat = net.forward(X)
        history.append(net.loss(y_hat, y))
        optimizer.step(net.p, net.backward(y))
    acc = np.mean((net.forward(X) > 0.5) == y)
    return history, acc


if __name__ == "__main__":
    X, y = make_circles()

    # Learning rates are tuned per optimizer; they are not directly comparable.
    optimizers = {
        "SGD (lr=0.5)":      lambda: SGD(0.5),
        "Momentum (lr=0.1)": lambda: Momentum(0.1),
        "Adam (lr=0.01)":    lambda: Adam(0.01),
    }

    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    print(f"{'activation':<10} {'optimizer':<20} {'final loss':>10} {'accuracy':>9}")
    for ax, act in zip(axes, ACTIVATIONS):
        for opt_name, make_opt in optimizers.items():
            hist, acc = train(act, make_opt(), X, y)
            ax.plot(hist, label=opt_name)
            print(f"{act:<10} {opt_name:<20} {hist[-1]:>10.4f} {acc:>9.3f}")
        ax.set_title(f"Activation: {act}")
        ax.set_xlabel("Epoch")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Binary cross-entropy")
    axes[0].legend()
    plt.tight_layout()
    plt.savefig("03_loss_curves.png", dpi=120)
    print("\nSaved 03_loss_curves.png")
