"""
Exercise 5: Embeddings + LSTM/GRU Classifier in PyTorch
Trains an nn.Embedding + nn.LSTM (or nn.GRU) classifier on the same IMDB split and
cleaning as exercise 2, then compares it with the best TF-IDF baseline from 02_results.json.

Padding is handled with pack_padded_sequence, so the RNN never processes padding tokens.
Usage: python 05_pytorch_lstm_gru_classifier.py data/IMDB\ Dataset.csv [lstm|gru]
"""
import sys
import json
import time
from collections import Counter
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pack_padded_sequence
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from text_pipeline import TextCleaner, load_imdb

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"
CELL = sys.argv[2] if len(sys.argv) > 2 else "lstm"
VOCAB_SIZE = 20_000
MAXLEN = 200
EMBED_DIM = 128
HIDDEN = 128
BATCH = 64
EPOCHS = 8
PATIENCE = 2
SEED = 42
PAD, UNK = 0, 1

torch.manual_seed(SEED)
np.random.seed(SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_vocab(token_lists):
    counts = Counter(t for toks in token_lists for t in toks)
    itos = ["<pad>", "<unk>"] + [w for w, c in counts.most_common(VOCAB_SIZE - 2) if c >= 2]
    return {w: i for i, w in enumerate(itos)}


def encode(token_lists, stoi):
    out = np.zeros((len(token_lists), MAXLEN), dtype=np.int64)
    for i, toks in enumerate(token_lists):
        ids = [stoi.get(t, UNK) for t in toks[:MAXLEN]]
        out[i, :len(ids)] = ids          # post-padding, lengths tracked separately
    return out


class TextDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        return self.X[i], self.y[i]


class SeqClassifier(nn.Module):
    def __init__(self, vocab_size, cell="lstm"):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, EMBED_DIM, padding_idx=PAD)
        rnn_cls = nn.LSTM if cell == "lstm" else nn.GRU
        self.rnn = rnn_cls(EMBED_DIM, HIDDEN, batch_first=True)
        self.drop = nn.Dropout(0.3)
        self.fc = nn.Linear(HIDDEN, 1)
        self.cell = cell

    def forward(self, x):
        lengths = (x != PAD).sum(dim=1).clamp(min=1).cpu()
        emb = self.emb(x)
        packed = pack_padded_sequence(emb, lengths, batch_first=True, enforce_sorted=False)
        _, h = self.rnn(packed)
        if self.cell == "lstm":
            h = h[0]                      # LSTM returns (h_n, c_n); we want h_n
        last = h[-1]                      # final hidden state of the last (only) layer, shape (B, H)
        return self.fc(self.drop(last)).squeeze(1)   # logits


def run_epoch(model, loader, criterion, optimizer=None):
    training = optimizer is not None
    model.train(training)
    total, n = 0.0, 0
    with torch.set_grad_enabled(training):
        for xb, yb in loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            logits = model(xb)
            loss = criterion(logits, yb)
            if training:
                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 1.0)   # guards against exploding gradients
                optimizer.step()
            total += loss.item() * len(xb)
            n += len(xb)
    return total / n


def predict(model, loader):
    model.eval()
    out = []
    with torch.no_grad():
        for xb, _ in loader:
            out.append(torch.sigmoid(model(xb.to(DEVICE))).cpu())
    return torch.cat(out).numpy()


if __name__ == "__main__":
    X_tr_raw, X_te_raw, y_tr, y_te = load_imdb(PATH)
    cleaner = TextCleaner(remove_stopwords=True, normalize=None)   # same cleaning as exercise 2
    tr_tok = [d.split() for d in cleaner.transform(X_tr_raw)]
    te_tok = [d.split() for d in cleaner.transform(X_te_raw)]

    # Validation split from the training data only; the test set stays untouched.
    idx_tr, idx_va = train_test_split(np.arange(len(tr_tok)), test_size=0.1,
                                      stratify=y_tr, random_state=SEED)
    stoi = build_vocab([tr_tok[i] for i in idx_tr])
    print(f"Vocab size: {len(stoi)}")

    enc_tr = encode([tr_tok[i] for i in idx_tr], stoi)
    enc_va = encode([tr_tok[i] for i in idx_va], stoi)
    enc_te = encode(te_tok, stoi)
    loaders = {
        "train": DataLoader(TextDataset(enc_tr, y_tr[idx_tr]), batch_size=BATCH, shuffle=True),
        "val": DataLoader(TextDataset(enc_va, y_tr[idx_va]), batch_size=256),
        "test": DataLoader(TextDataset(enc_te, y_te), batch_size=256),
    }

    model = SeqClassifier(len(stoi), CELL).to(DEVICE)
    print(f"{CELL.upper()} classifier params: {sum(p.numel() for p in model.parameters()):,}  "
          f"device: {DEVICE}")
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    best_val, best_state, wait = float("inf"), None, 0
    t0 = time.time()
    for epoch in range(1, EPOCHS + 1):
        tr_loss = run_epoch(model, loaders["train"], criterion, optimizer)
        va_loss = run_epoch(model, loaders["val"], criterion)
        print(f"epoch {epoch}  train_loss={tr_loss:.4f}  val_loss={va_loss:.4f}")
        if va_loss < best_val - 1e-4:
            best_val, wait = va_loss, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            wait += 1
            if wait >= PATIENCE:
                print("Early stopping")
                break
    print(f"Training time: {time.time() - t0:.0f}s")
    model.load_state_dict(best_state)

    probs = predict(model, loaders["test"])
    pred = (probs > 0.5).astype(int)
    rnn_row = {"model": f"{CELL.upper()} (PyTorch)", "accuracy": accuracy_score(y_te, pred),
               "f1": f1_score(y_te, pred), "roc_auc": roc_auc_score(y_te, probs)}

    with open("02_results.json") as f:
        baseline = json.load(f)
    tfidf_rows = [r for r in baseline["rows"] if r["features"] == "TF-IDF"]
    best_tfidf = max(tfidf_rows, key=lambda r: r["accuracy"])

    print("\n=== Comparison on the same test split ===")
    print(f"{'model':<28}{'accuracy':>10}{'f1':>8}{'roc_auc':>10}")
    print(f"{'TF-IDF + ' + best_tfidf['classifier']:<28}"
          f"{best_tfidf['accuracy']:>10.4f}{best_tfidf['f1']:>8.4f}{best_tfidf['roc_auc']:>10.4f}")
    print(f"{rnn_row['model']:<28}{rnn_row['accuracy']:>10.4f}{rnn_row['f1']:>8.4f}{rnn_row['roc_auc']:>10.4f}")

    torch.save(model.state_dict(), f"seq_{CELL}.pt")
    with open(f"05_{CELL}_results.json", "w") as f:
        json.dump(rnn_row, f, indent=2, default=float)
    print(f"Saved seq_{CELL}.pt and 05_{CELL}_results.json")
