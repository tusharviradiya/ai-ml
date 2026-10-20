"""
Exercise 2: LoRA / QLoRA Fine-Tuning with SFTTrainer.
Trains a LoRA adapter on the Acme Sync support data and logs training and validation loss.
Also reports loss on the held-out test split. Every hyperparameter used in the experiments is
a command-line argument, so 04_hparam_experiments.py can call this script directly.

Requires trl >= 0.20 (for the max_length argument on SFTConfig).

Usage:
  python 02_train_lora.py                           # baseline, rank 16, lr 2e-4
  python 02_train_lora.py --rank 4 --out runs/r4
  python 02_train_lora.py --qlora                   # 4-bit base (needs CUDA + bitsandbytes)
"""
import argparse
import json
import os
import random
import time
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
from common import BASE_MODEL, read_jsonl, to_prompt_completion

TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--train", default="data/train.jsonl")
    p.add_argument("--val", default="data/val.jsonl")
    p.add_argument("--test", default="data/test.jsonl")
    p.add_argument("--out", default="runs/baseline")
    p.add_argument("--rank", type=int, default=16)
    p.add_argument("--alpha", type=int, default=None, help="defaults to 2 * rank")
    p.add_argument("--lora-dropout", type=float, default=0.0)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--grad-accum", type=int, default=1)
    p.add_argument("--scheduler", default="cosine")
    p.add_argument("--warmup", type=float, default=0.03)
    p.add_argument("--weight-decay", type=float, default=0.0)
    p.add_argument("--max-len", type=int, default=512)
    p.add_argument("--max-train", type=int, default=None, help="random subsample of the train set")
    p.add_argument("--eval-steps", type=int, default=50)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--qlora", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = parse()
    alpha = args.alpha or 2 * args.rank
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    os.makedirs(args.out, exist_ok=True)

    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    train_rows = read_jsonl(args.train)
    if args.max_train:
        train_rows = random.Random(args.seed).sample(train_rows, min(args.max_train, len(train_rows)))
    val_rows, test_rows = read_jsonl(args.val), read_jsonl(args.test)
    to_ds = lambda rows: Dataset.from_list([to_prompt_completion(r) for r in rows])
    train_ds, val_ds, test_ds = to_ds(train_rows), to_ds(val_rows), to_ds(test_rows)
    print(f"train={len(train_ds)} val={len(val_ds)} test={len(test_ds)}")

    # Show one rendered example, so you can see the chat template the model is trained on.
    example = train_ds[0]["prompt"] + train_ds[0]["completion"]
    print("---- rendered training example ----")
    print(tok.apply_chat_template(example, tokenize=False))
    print("-----------------------------------")

    if args.qlora:
        from transformers import BitsAndBytesConfig
        from peft import prepare_model_for_kbit_training
        bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype=torch.bfloat16)
        model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, quantization_config=bnb,
                                                     device_map="auto")
        model = prepare_model_for_kbit_training(model)
    else:
        # fp32 everywhere, so this run is directly comparable to 05_under_the_hood.py.
        model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float32)

    peft_config = LoraConfig(r=args.rank, lora_alpha=alpha, lora_dropout=args.lora_dropout,
                             target_modules=TARGET_MODULES, bias="none", task_type="CAUSAL_LM")

    cfg = SFTConfig(
        output_dir=os.path.join(args.out, "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type=args.scheduler,
        warmup_ratio=args.warmup,
        weight_decay=args.weight_decay,
        max_grad_norm=1.0,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=args.eval_steps,
        save_strategy="no",
        max_length=args.max_len,
        seed=args.seed,
        report_to="none",
    )
    trainer = SFTTrainer(model=model, args=cfg, train_dataset=train_ds, eval_dataset=val_ds,
                         peft_config=peft_config, processing_class=tok)
    trainer.model.print_trainable_parameters()

    t0 = time.time()
    trainer.train()
    train_time = time.time() - t0

    test_metrics = trainer.evaluate(eval_dataset=test_ds, metric_key_prefix="test")
    print(f"\nTest loss: {test_metrics['test_loss']:.4f}")

    adapter_dir = os.path.join(args.out, "adapter")
    trainer.model.save_pretrained(adapter_dir)      # saves only the LoRA weights
    tok.save_pretrained(adapter_dir)
    adapter_kb = sum(os.path.getsize(os.path.join(dp, f))
                     for dp, _, fs in os.walk(adapter_dir) for f in fs) / 1e3
    trainable = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)

    run_log = {
        "config": {**vars(args), "alpha": alpha, "target_modules": TARGET_MODULES},
        "n_train": len(train_ds),
        "trainable_params": trainable,
        "adapter_kb": adapter_kb,
        "train_time_sec": train_time,
        "test_loss": test_metrics["test_loss"],
        "log_history": trainer.state.log_history,
    }
    with open(os.path.join(args.out, "run_log.json"), "w") as f:
        json.dump(run_log, f, indent=2, default=float)
    print(f"Trainable params: {trainable:,}  Adapter: {adapter_kb:.0f} KB  "
          f"Time: {train_time:.0f}s  Saved {args.out}/run_log.json")
