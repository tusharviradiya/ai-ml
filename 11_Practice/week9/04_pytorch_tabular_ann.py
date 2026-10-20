"""
Exercise 4: PyTorch Warm-up
Re-implements the week-6 Titanic ANN in PyTorch with a custom Dataset, DataLoader,
and a manual training loop. The architecture (32-16 ReLU, sigmoid output), split,
and preprocessing match the Keras version, so results should be similar.

Usage: python 04_pytorch_tabular_ann.py data/train.csv
"""
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/titanic_train.csv"
NUM_COLS = ["Age", "SibSp", "Parch", "Fare", "FamilySize"]
CAT_COLS = ["Pclass", "Sex", "Embarked"]
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Same preprocessing as week-6/titanic_prep.py, so the splits and features match.
def make_preprocessor():
    num = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    cat = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                    ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([("num", num, NUM_COLS), ("cat", cat, CAT_COLS)], sparse_threshold=0)


def load_splits(path):
    df = pd.read_csv(path)
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    X, y = df[NUM_COLS + CAT_COLS], df["Survived"].values
    X_tv, X_te, y_tv, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    X_tr, X_va, y_tr, y_va = train_test_split(X_tv, y_tv, test_size=0.2, stratify=y_tv, random_state=SEED)
    prep = make_preprocessor().fit(X_tr)
    f = lambda A: prep.transform(A).astype(np.float32)
    return (f(X_tr), y_tr), (f(X_va), y_va), (f(X_te), y_te)


class TabularDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def build_model(n_in):
    # Outputs raw logits. BCEWithLogitsLoss applies the sigmoid internally, which is numerically
    # more stable than a sigmoid layer followed by BCELoss.
    return nn.Sequential(
        nn.Linear(n_in, 32), nn.ReLU(),
        nn.Linear(32, 16), nn.ReLU(),
        nn.Linear(16, 1),
    )


def predict_proba(model, loader):
    model.eval()
    probs = []
    with torch.no_grad():
        for xb, _ in loader:
            probs.append(torch.sigmoid(model(xb.to(DEVICE))).cpu())
    return torch.cat(probs).numpy().ravel()


if __name__ == "__main__":
    (X_tr, y_tr), (X_va, y_va), (X_te, y_te) = load_splits(PATH)
    print("Feature matrix:", X_tr.shape, "device:", DEVICE)

    train_loader = DataLoader(TabularDataset(X_tr, y_tr), batch_size=32, shuffle=True)
    val_loader = DataLoader(TabularDataset(X_va, y_va), batch_size=256)
    test_loader = DataLoader(TabularDataset(X_te, y_te), batch_size=256)

    model = build_model(X_tr.shape[1]).to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # Manual training loop with early stopping on validation loss.
    best_val, best_state, wait, patience = float("inf"), None, 0, 25
    history = {"train": [], "val": []}
    for epoch in range(1, 501):
        model.train()
        running = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            optimizer.step()
            running += loss.item() * len(xb)
        history["train"].append(running / len(train_loader.dataset))

        model.eval()
        with torch.no_grad():
            val_loss = sum(criterion(model(xb.to(DEVICE)), yb.to(DEVICE)).item() * len(xb)
                           for xb, yb in val_loader) / len(val_loader.dataset)
        history["val"].append(val_loss)

        if val_loss < best_val - 1e-4:
            best_val, wait = val_loss, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            wait += 1
            if wait >= patience:
                print(f"Early stop at epoch {epoch} (best epoch {epoch - patience})")
                break

    model.load_state_dict(best_state)
    probs = predict_proba(model, test_loader)
    pred = (probs > 0.5).astype(int)
    print("\n=== PyTorch test results (same split as Keras week 6) ===")
    print(f"Accuracy: {accuracy_score(y_te, pred):.3f}")
    print(f"F1:       {f1_score(y_te, pred):.3f}")
    print(f"ROC-AUC:  {roc_auc_score(y_te, probs):.3f}")
    print(f"Params:   {sum(p.numel() for p in model.parameters())}")
    print("\nCompare with the Keras test numbers from week-6/README.md. Expect them to be close, "
          "not identical: the weight initializers and random shuffle order differ.")
    torch.save(model.state_dict(), "pytorch_tabular_ann.pt")
