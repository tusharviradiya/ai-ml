"""
Exercise 3: Before vs. After
Runs the base model and the fine-tuned (base + LoRA adapter) model on:
  1. The 25 hand-written evaluation prompts (unseen by training), side by side in 03_before_after.md
  2. The first 100 held-out test conversations, scored by token-level F1 against the reference reply

Decoding is greedy, so the two models are compared on identical settings.
Usage: python 03_before_after.py [adapter_dir]
"""
import json
import re
import sys
from collections import Counter
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from common import BASE_MODEL, SYSTEM_PROMPT, read_jsonl

ADAPTER = sys.argv[1] if len(sys.argv) > 1 else "runs/baseline/adapter"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_NEW = 200


def toks(s):
    return re.findall(r"[a-z0-9']+", s.lower())


def token_f1(pred, ref):
    p, r = Counter(toks(pred)), Counter(toks(ref))
    overlap = sum((p & r).values())
    if overlap == 0:
        return 0.0
    prec, rec = overlap / sum(p.values()), overlap / sum(r.values())
    return 2 * prec * rec / (prec + rec)


@torch.no_grad()
def generate(model, tok, messages):
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    enc = tok(text, return_tensors="pt", add_special_tokens=False).to(DEVICE)
    out = model.generate(**enc, max_new_tokens=MAX_NEW, do_sample=False,
                         pad_token_id=tok.pad_token_id)
    return tok.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()


if __name__ == "__main__":
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32).to(DEVICE).eval()
    ft = PeftModel.from_pretrained(base, ADAPTER).eval()   # wraps the same base weights

    def both(messages):
        with ft.disable_adapter():                 # base model: adapter switched off
            b = generate(ft, tok, messages)
        f = generate(ft, tok, messages)            # fine-tuned: adapter on
        return b, f

    # ---- 1. Unseen prompts, side by side ----
    eval_rows = read_jsonl("data/eval_prompts.jsonl")
    rows = []
    for r in eval_rows:
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": r["prompt"]}]
        b, f = both(msgs)
        rows.append({**r, "base": b, "finetuned": f})
        print(f"[{r['category']}] {r['prompt']}\n  base: {b[:140]}\n  ft:   {f[:140]}\n")

    with open("03_before_after.md", "w", encoding="utf-8") as fh:
        fh.write("# Before vs. after on unseen prompts\n\n")
        for r in rows:
            fh.write(f"## {r['id'] + 1}. ({r['category']}) {r['prompt']}\n\n"
                     f"**Base model**\n\n> {r['base']}\n\n"
                     f"**Fine-tuned**\n\n> {r['finetuned']}\n\n---\n\n")

    # Proxy checks on the unseen prompts
    in_scope = [r for r in rows if r["category"] != "off topic"]
    off = [r for r in rows if r["category"] == "off topic"]
    mention = lambda rs, key: np.mean(["Acme Sync" in r[key] for r in rs])
    refuse = lambda rs, key: np.mean(["only help" in r[key].lower() or "can't help" in r[key].lower()
                                      or "outside" in r[key].lower() for r in rs])
    print("Share of replies naming Acme Sync (in-scope prompts): "
          f"base={mention(in_scope, 'base'):.2f}  ft={mention(in_scope, 'finetuned'):.2f}")
    print("Share of off-topic prompts redirected to Acme Sync: "
          f"base={refuse(off, 'base'):.2f}  ft={refuse(off, 'finetuned'):.2f}")
    print("Avg reply words: base={:.1f}  ft={:.1f}".format(
        np.mean([len(r['base'].split()) for r in rows]),
        np.mean([len(r['finetuned'].split()) for r in rows])))

    # ---- 2. Held-out test set with reference replies ----
    test = read_jsonl("data/test.jsonl")[:100]
    f1_base, f1_ft = [], []
    for ex in test:
        msgs = ex["messages"][:-1]
        ref = ex["messages"][-1]["content"]
        b, f = both(msgs)
        f1_base.append(token_f1(b, ref))
        f1_ft.append(token_f1(f, ref))
    print(f"\nTest set token-F1 (n={len(test)}): base={np.mean(f1_base):.3f}  "
          f"fine-tuned={np.mean(f1_ft):.3f}")

    with open("03_results.json", "w") as fh:
        json.dump({"test_token_f1_base": float(np.mean(f1_base)),
                   "test_token_f1_ft": float(np.mean(f1_ft)),
                   "n_test": len(test), "eval_prompts": rows}, fh, indent=2)
    print("Saved 03_before_after.md and 03_results.json")
