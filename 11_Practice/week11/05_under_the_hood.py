"""
Exercise 5 (optional): LoRA from scratch in PyTorch.
Implements LoRA by hand (no peft, no SFTTrainer): a LoRALinear wrapper, a completion-only
loss, a batch loop with AdamW, and a validation pass. Then compares its loss curve with the
SFTTrainer run in runs/match.

Matching the trainer requires running this once first:
  python 02_train_lora.py --out runs/match --scheduler constant --warmup 0 --lora-dropout 0

Expect close agreement, not bit-for-bit equality. The two runs shuffle the data differently,
and the trainer's tokenization of prompt and completion may differ by a token or two.

Usage: python 05_under_the_hood.py
"""
import json
import math
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from common import BASE_MODEL, read_jsonl

TARGETS = {"q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"}
RANK, ALPHA = 16, 32
LR, EPOCHS, BATCH = 2e-4, 3, 8
MAX_LEN, SEED = 512, 42
LOG_STEPS, EVAL_STEPS, CLIP = 10, 50, 1.0
COMPARE_RUN = "runs/match"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LoRALinear(nn.Module):
    """
    y = W x + (alpha / r) * B (A x)
    W is frozen. A is r x in, initialized with Kaiming uniform. B is out x r, initialized to zero,
    so the wrapped layer starts out exactly equal to the base layer.
    """

    def __init__(self, base: nn.Linear, r: int, alpha: float):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False
        self.A = nn.Parameter(torch.empty(r, base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.t() @ self.B.t()) * self.scale


def inject_lora(model):
    for parent in list(model.modules()):
        for name, child in list(parent.named_children()):
            if name in TARGETS and isinstance(child, nn.Linear):
                setattr(parent, name, LoRALinear(child, RANK, ALPHA))


def test_lora_math():
    lin = nn.Linear(16, 8)
    x = torch.randn(4, 16)
    wrapped = LoRALinear(lin, r=4, alpha=8)
    assert torch.allclose(wrapped(x), lin(x), atol=1e-6), "B = 0 must reproduce the base output"
    wrapped.B.data.normal_()
    delta_w = wrapped.scale * (wrapped.B @ wrapped.A)          # explicit low-rank update
    assert torch.allclose(wrapped(x), lin(x) + x @ delta_w.t(), atol=1e-5)
    print("LoRA math checks passed")


def encode(tok, rec):
    """Tokenize one conversation; labels are -100 on the prompt, so loss covers only the reply."""
    msgs = rec["messages"]
    prompt_text = tok.apply_chat_template(msgs[:-1], tokenize=False, add_generation_prompt=True)
    full_text = tok.apply_chat_template(msgs, tokenize=False)
    p_ids = tok(prompt_text, add_special_tokens=False)["input_ids"]
    f_ids = tok(full_text, add_special_tokens=False)["input_ids"]
    if f_ids[:len(p_ids)] != p_ids:
        return None                                              # prefix mismatch; skip
    labels = [-100] * len(p_ids) + f_ids[len(p_ids):]
    return f_ids[:MAX_LEN], labels[:MAX_LEN]


def collate(batch, pad_id):
    L = max(len(ids) for ids, _ in batch)
    ids = torch.full((len(batch), L), pad_id, dtype=torch.long)
    lab = torch.full((len(batch), L), -100, dtype=torch.long)
    att = torch.zeros((len(batch), L), dtype=torch.long)
    for k, (i, l) in enumerate(batch):
        n = len(i)
        ids[k, :n] = torch.tensor(i)
        lab[k, :n] = torch.tensor(l)
        att[k, :n] = 1
    return ids, att, lab


def loss_fn(logits, labels):
    # Next-token prediction: position t predicts token t+1. Mean over non-masked tokens.
    return F.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)),
                           labels[:, 1:].reshape(-1), ignore_index=-100)


@torch.no_grad()
def eval_loss(model, loader):
    model.eval()
    losses = []
    for ids, att, lab in loader:
        logits = model(input_ids=ids.to(DEVICE), attention_mask=att.to(DEVICE)).logits
        losses.append(loss_fn(logits, lab.to(DEVICE)).item())
    model.train()
    return sum(losses) / len(losses)            # average of batch means, as the Trainer does


def check_config(path):
    with open(path) as f:
        cfg = json.load(f)["config"]
    expected = {"scheduler": "constant", "warmup": 0.0, "lora_dropout": 0.0, "weight_decay": 0.0,
                "batch": BATCH, "epochs": EPOCHS, "lr": LR, "rank": RANK, "max_len": MAX_LEN,
                "grad_accum": 1, "seed": SEED}
    bad = {k: (cfg.get(k), v) for k, v in expected.items() if cfg.get(k) != v}
    if bad:
        print("WARNING: comparison run config differs from this script (run, expected):", bad)
    else:
        print("Comparison run config matches this script.")


if __name__ == "__main__":
    test_lora_math()
    torch.manual_seed(SEED)

    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    train_rows = read_jsonl("data/train.jsonl")
    val_rows = read_jsonl("data/val.jsonl")
    enc_tr = [e for e in (encode(tok, r) for r in train_rows) if e]
    enc_va = [e for e in (encode(tok, r) for r in val_rows) if e]
    print(f"Encoded train={len(enc_tr)} val={len(enc_va)}")

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)
    for p in model.parameters():
        p.requires_grad = False
    inject_lora(model)
    model.to(DEVICE)
    trainable = [p for p in model.parameters() if p.requires_grad]
    print("Trainable LoRA params:", sum(p.numel() for p in trainable))

    opt = torch.optim.AdamW(trainable, lr=LR, weight_decay=0.0)   # constant LR, matching the run
    gen = torch.Generator().manual_seed(SEED)
    collate_fn = lambda b: collate(b, tok.pad_token_id)
    train_loader = DataLoader(enc_tr, batch_size=BATCH, shuffle=True, generator=gen, collate_fn=collate_fn)
    val_loader = DataLoader(enc_va, batch_size=BATCH, shuffle=False, collate_fn=collate_fn)

    log_train, log_eval, window, step = [], [], [], 0
    model.train()
    t0 = time.time()
    for epoch in range(EPOCHS):
        for ids, att, lab in train_loader:
            step += 1
            logits = model(input_ids=ids.to(DEVICE), attention_mask=att.to(DEVICE)).logits
            loss = loss_fn(logits, lab.to(DEVICE))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(trainable, CLIP)
            opt.step()
            window.append(loss.item())
            if step % LOG_STEPS == 0:
                log_train.append({"step": step, "loss": sum(window) / len(window)})   # windowed mean
                window = []
            if step % EVAL_STEPS == 0:
                log_eval.append({"step": step, "eval_loss": eval_loss(model, val_loader)})
                print(f"step {step}  train={log_train[-1]['loss']:.4f}  val={log_eval[-1]['eval_loss']:.4f}")
    train_time = time.time() - t0

    lora_state = {n: p.detach().cpu() for n, p in model.named_parameters() if p.requires_grad}
    torch.save(lora_state, "runs_manual_lora.pt")
    with open("runs_manual_log.json", "w") as f:
        json.dump({"train": log_train, "eval": log_eval, "train_time_sec": train_time}, f, indent=2)
    print(f"Manual loop finished in {train_time:.0f}s")

    # ---- Compare against SFTTrainer ----
    try:
        check_config(f"{COMPARE_RUN}/run_log.json")
        with open(f"{COMPARE_RUN}/run_log.json") as f:
            trl = json.load(f)["log_history"]
    except FileNotFoundError:
        print(f"{COMPARE_RUN}/run_log.json not found. Run the comparison command in the docstring first.")
        raise SystemExit(0)

    trl_train = {e["step"]: e["loss"] for e in trl if "loss" in e and "eval_loss" not in e and "step" in e}
    trl_eval = {e["step"]: e["eval_loss"] for e in trl if "eval_loss" in e}

    print("\nstep   trainer_loss  manual_loss  rel_diff")
    rel = []
    for s, m in [(e["step"], e["loss"]) for e in log_train]:
        if s in trl_train:
            r = abs(m - trl_train[s]) / trl_train[s]
            rel.append(r)
            print(f"{s:>4}   {trl_train[s]:>11.4f}  {m:>11.4f}  {r:>7.2%}")
    print("\nstep   trainer_eval  manual_eval  rel_diff")
    for e in log_eval:
        s = e["step"]
        if s in trl_eval:
            r = abs(e["eval_loss"] - trl_eval[s]) / trl_eval[s]
            rel.append(r)
            print(f"{s:>4}   {trl_eval[s]:>11.4f}  {e['eval_loss']:>11.4f}  {r:>7.2%}")
    if rel:
        mean_rel = sum(rel) / len(rel)
        verdict = "close agreement" if mean_rel < 0.05 else "noticeable gap; see README for likely causes"
        print(f"\nMean relative difference: {mean_rel:.2%}  ->  {verdict}")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot([e["step"] for e in trl if "loss" in e and "eval_loss" not in e and "step" in e],
            [e["loss"] for e in trl if "loss" in e and "eval_loss" not in e and "step" in e],
            label="SFTTrainer (train)", alpha=0.8)
    ax.plot([e["step"] for e in log_train], [e["loss"] for e in log_train],
            label="manual loop (train)", alpha=0.8, linestyle="--")
    ax.plot([e["step"] for e in trl if "eval_loss" in e], [e["eval_loss"] for e in trl if "eval_loss" in e],
            "o-", label="SFTTrainer (val)")
    ax.plot([e["step"] for e in log_eval], [e["eval_loss"] for e in log_eval], "s--", label="manual loop (val)")
    ax.set_xlabel("Step"); ax.set_ylabel("Loss"); ax.set_title("LoRA: SFTTrainer vs manual loop")
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("05_loss_comparison.png", dpi=120)
    print("Saved runs_manual_log.json, runs_manual_lora.pt, 05_loss_comparison.png")
