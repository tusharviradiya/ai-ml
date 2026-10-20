"""
Exercise 2b: Re-implement the same fine-tuning with a manual PyTorch loop.
Same model, data, split, hyperparameters, and metrics as 02_finetune_trainer.py, so the
two results should be close. Shows what Trainer does for you: batching, mixed precision,
gradient clipping, scheduling, evaluation, and checkpoint selection.

Usage: python 03_finetune_pytorch_loop.py data/IMDB\ Dataset.csv [subset_size]
"""
import sys
import json
import time
import os
import copy
import numpy as np
import torch
from torch.utils.data import DataLoader
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          DataCollatorWithPadding, get_linear_schedule_with_warmup)
from torch.optim import AdamW
from data_utils import load_imdb_split, to_transformer_text, MODEL_NAME, MAX_LEN

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"
SUBSET = int(sys.argv[2]) if len(sys.argv) > 2 else None
OUT_DIR = "distilbert_manual"
SEED = 42
EPOCHS = 2
BATCH = 16
EVAL_BATCH = 64
LR = 2e-5
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.06
CLIP_NORM = 1.0
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
USE_AMP = DEVICE.type == "cuda"


def make_dataset(tok, texts, labels):
    enc = tok(list(texts), truncation=True, max_length=MAX_LEN)
    enc["labels"] = [int(l) for l in labels]
    return Dataset.from_dict(dict(enc))


def evaluate(model, loader):
    model.eval()
    probs, labels = [], []
    with torch.no_grad(), torch.autocast(device_type=DEVICE.type, enabled=USE_AMP):
        for batch in loader:
            labels.append(batch.pop("labels").numpy())
            batch = {k: v.to(DEVICE) for k, v in batch.items()}
            logits = model(**batch).logits.float()
            probs.append(torch.softmax(logits, dim=-1)[:, 1].cpu().numpy())
    return np.concatenate(probs), np.concatenate(labels)


def metrics_from(probs, labels):
    preds = (probs > 0.5).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    return {"accuracy": accuracy_score(labels, preds), "precision": p,
            "recall": r, "f1": f1, "roc_auc": roc_auc_score(labels, probs)}


if __name__ == "__main__":
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    X_tr, X_te, y_tr, y_te = load_imdb_split(PATH)
    if SUBSET:
        X_tr, y_tr = X_tr[:SUBSET], y_tr[:SUBSET]
        X_te, y_te = X_te[:SUBSET // 4], y_te[:SUBSET // 4]
    idx_tr, idx_va = train_test_split(np.arange(len(X_tr)), test_size=0.1,
                                      stratify=y_tr, random_state=SEED)

    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    collator = DataCollatorWithPadding(tok, return_tensors="pt")
    ds_tr = make_dataset(tok, to_transformer_text(X_tr[idx_tr]), y_tr[idx_tr])
    ds_va = make_dataset(tok, to_transformer_text(X_tr[idx_va]), y_tr[idx_va])
    ds_te = make_dataset(tok, to_transformer_text(X_te), y_te)

    train_loader = DataLoader(ds_tr, batch_size=BATCH, shuffle=True, collate_fn=collator)
    val_loader = DataLoader(ds_va, batch_size=EVAL_BATCH, collate_fn=collator)
    test_loader = DataLoader(ds_te, batch_size=EVAL_BATCH, collate_fn=collator)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2).to(DEVICE)

    # Weight decay is not applied to biases and LayerNorm weights (standard BERT practice).
    no_decay = ("bias", "LayerNorm.weight")
    groups = [
        {"params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         "weight_decay": WEIGHT_DECAY},
        {"params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
         "weight_decay": 0.0},
    ]
    optimizer = AdamW(groups, lr=LR)
    total_steps = EPOCHS * len(train_loader)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=int(WARMUP_RATIO * total_steps), num_training_steps=total_steps)
    scaler = torch.amp.GradScaler("cuda", enabled=USE_AMP)

    best_f1, best_state, best_epoch = -1.0, None, None
    t0 = time.time()
    for epoch in range(1, EPOCHS + 1):
        model.train()
        running, seen = 0.0, 0
        for step, batch in enumerate(train_loader, start=1):
            batch = {k: v.to(DEVICE) for k, v in batch.items()}
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast(device_type=DEVICE.type, enabled=USE_AMP):
                loss = model(**batch).loss
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP_NORM)
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()
            running += loss.item() * batch["labels"].size(0)
            seen += batch["labels"].size(0)
            if step % 200 == 0:
                print(f"epoch {epoch} step {step}/{len(train_loader)}  loss={running / seen:.4f}")

        probs, labels = evaluate(model, val_loader)
        val = metrics_from(probs, labels)
        print(f"epoch {epoch}  train_loss={running / seen:.4f}  "
              f"val_acc={val['accuracy']:.4f}  val_f1={val['f1']:.4f}")
        if val["f1"] > best_f1:
            best_f1, best_epoch = val["f1"], epoch
            best_state = copy.deepcopy(model.state_dict())

    train_time = time.time() - t0
    model.load_state_dict(best_state)
    print(f"\nBest epoch by validation F1: {best_epoch}")

    probs, labels = evaluate(model, test_loader)
    test_metrics = metrics_from(probs, labels)
    print("Test:", {k: round(float(v), 4) for k, v in test_metrics.items()})

    model.save_pretrained(OUT_DIR)
    tok.save_pretrained(OUT_DIR)
    size_mb = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT_DIR) for f in fs) / 1e6
    with open("03_manual_results.json", "w") as f:
        json.dump({"method": "manual loop", "train_time_sec": train_time, "model_size_mb": size_mb,
                   "best_epoch": best_epoch, **{k: float(v) for k, v in test_metrics.items()}},
                  f, indent=2)
    print(f"Training time: {train_time:.0f}s  Model size: {size_mb:.1f} MB")
    print(f"Saved {OUT_DIR}/ and 03_manual_results.json")
