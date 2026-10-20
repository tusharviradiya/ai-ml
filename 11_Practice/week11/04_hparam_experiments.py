"""
Exercise 4: Hyperparameter Experiments
Runs one-factor-at-a-time experiments around the baseline (rank 16, lr 2e-4, full train set),
changing one thing per run. Each run is a separate call to 02_train_lora.py.

LoRA scaling is alpha / rank. Alpha is set to 2 * rank in every run, so changing the rank does
not also change the effective update scale. Otherwise the rank effect would be confounded.

Usage:
  python 04_hparam_experiments.py               # all runs, skipping ones already finished
  python 04_hparam_experiments.py --only rank_4 lr_1e-3
"""
import argparse
import json
import os
import subprocess
import sys
import matplotlib.pyplot as plt
import pandas as pd

EXPERIMENTS = [
    ("baseline", []),                              # rank 16, lr 2e-4, full train set, cosine
    ("rank_4", ["--rank", "4"]),
    ("rank_64", ["--rank", "64"]),
    ("lr_5e-5", ["--lr", "5e-5"]),
    ("lr_1e-3", ["--lr", "1e-3"]),
    ("data_300", ["--max-train", "300"]),
    ("data_100", ["--max-train", "100"]),
]


def summarize(name, log):
    cfg = log["config"]
    evals = [e["eval_loss"] for e in log["log_history"] if "eval_loss" in e]
    return {
        "run": name,
        "rank": cfg["rank"], "lr": cfg["lr"], "n_train": log["n_train"],
        "trainable_params": log["trainable_params"],
        "best_val_loss": min(evals),
        "final_val_loss": evals[-1],
        "test_loss": log["test_loss"],
        "train_time_sec": round(log["train_time_sec"]),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()

    selected = [(n, a) for n, a in EXPERIMENTS if args.only is None or n in args.only]
    for name, extra in selected:
        out = f"runs/{name}"
        if os.path.exists(os.path.join(out, "run_log.json")):
            print(f"[skip] {name} already finished")
            continue
        cmd = [sys.executable, "02_train_lora.py", "--out", out, *extra]
        print(f"\n=== {name}: {' '.join(extra) or '(baseline)'} ===")
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"[fail] {name} exited with {res.returncode}; continuing")

    rows, curves = [], {}
    for name, _ in EXPERIMENTS:
        path = f"runs/{name}/run_log.json"
        if not os.path.exists(path):
            continue
        with open(path) as f:
            log = json.load(f)
        rows.append(summarize(name, log))
        curves[name] = [(e["step"], e["eval_loss"]) for e in log["log_history"] if "eval_loss" in e]

    if not rows:
        print("No finished runs found.")
        sys.exit(0)

    df = pd.DataFrame(rows)
    pd.set_option("display.width", 160)
    print("\n=== Experiment summary ===")
    print(df.round(4).to_string(index=False))
    df.to_csv("04_experiments.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    for name, pts in curves.items():
        steps, losses = zip(*pts)
        ax.plot(steps, losses, marker="o", ms=3, label=name)
    ax.set_xlabel("Step"); ax.set_ylabel("Validation loss")
    ax.set_title("Validation loss by experiment")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("04_val_loss_experiments.png", dpi=120)
    print("Saved 04_experiments.csv and 04_val_loss_experiments.png")
