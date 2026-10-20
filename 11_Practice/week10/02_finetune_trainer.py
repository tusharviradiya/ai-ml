"""
Exercise 2a: Fine-tune DistilBERT with the Hugging Face Trainer API.
Binary sentiment on IMDB (same split as week 9). Metrics: accuracy, precision, recall,
F1, and ROC-AUC on the held-out test set. Validation is carved from train, and the best
epoch is chosen by validation F1.

Usage: python 02_finetune_trainer.py data/IMDB\ Dataset.csv [subset_size]
"""
import sys
import json
import time
import os
import numpy as np
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, DataCollatorWithPadding)
from data_utils import load_imdb_split, to_transformer_text, MODEL_NAME, MAX_LEN

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"
SUBSET = int(sys.argv[2]) if len(sys.argv) > 2 else None   # quick test runs, e.g. 2000
OUT_DIR = "distilbert_imdb"
SEED = 42


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    probs = torch.softmax(torch.tensor(logits), dim=-1)[:, 1].numpy()
    preds = (probs > 0.5).astype(int)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    return {"accuracy": accuracy_score(labels, preds), "precision": p,
            "recall": r, "f1": f1, "roc_auc": roc_auc_score(labels, probs)}


def make_dataset(tok, texts, labels):
    enc = tok(list(texts), truncation=True, max_length=MAX_LEN)
    enc["labels"] = [int(l) for l in labels]
    return Dataset.from_dict(dict(enc))


if __name__ == "__main__":
    torch.manual_seed(SEED)
    X_tr, X_te, y_tr, y_te = load_imdb_split(PATH)
    if SUBSET:
        X_tr, y_tr = X_tr[:SUBSET], y_tr[:SUBSET]
        X_te, y_te = X_te[:SUBSET // 4], y_te[:SUBSET // 4]
    idx_tr, idx_va = train_test_split(np.arange(len(X_tr)), test_size=0.1,
                                      stratify=y_tr, random_state=SEED)

    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    ds_tr = make_dataset(tok, to_transformer_text(X_tr[idx_tr]), y_tr[idx_tr])
    ds_va = make_dataset(tok, to_transformer_text(X_tr[idx_va]), y_tr[idx_va])
    ds_te = make_dataset(tok, to_transformer_text(X_te), y_te)
    print(f"Train {len(ds_tr)}  Val {len(ds_va)}  Test {len(ds_te)}")

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

    args = TrainingArguments(
        output_dir="runs/distilbert",
        num_train_epochs=2,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_ratio=0.06,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        logging_steps=100,
        fp16=torch.cuda.is_available(),
        report_to="none",
        seed=SEED,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds_tr,
        eval_dataset=ds_va,
        data_collator=DataCollatorWithPadding(tok),   # pads each batch dynamically
        processing_class=tok,
        compute_metrics=compute_metrics,
    )

    t0 = time.time()
    trainer.train()
    train_time = time.time() - t0

    print("\nEvaluating on test set")
    out = trainer.predict(ds_te)
    test_metrics = compute_metrics((out.predictions, out.label_ids))
    print({k: round(float(v), 4) for k, v in test_metrics.items()})

    trainer.save_model(OUT_DIR)
    tok.save_pretrained(OUT_DIR)
    size_mb = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT_DIR) for f in fs) / 1e6
    with open("02_trainer_results.json", "w") as f:
        json.dump({"method": "Trainer", "train_time_sec": train_time, "model_size_mb": size_mb,
                   **{k: float(v) for k, v in test_metrics.items()}}, f, indent=2)
    print(f"Training time: {train_time:.0f}s  Model size: {size_mb:.1f} MB")
    print(f"Saved {OUT_DIR}/ and 02_trainer_results.json")
