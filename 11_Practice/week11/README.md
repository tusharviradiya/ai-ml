# Week 11: Dataset Preparation, LoRA Fine-Tuning, and Under the Hood

## Setup
```bash
pip install "transformers>=4.45" "trl>=0.20" peft datasets accelerate torch matplotlib pandas
# Optional, for QLoRA only (CUDA required):
pip install bitsandbytes
```
A GPU is needed for practical runs. The base model is Qwen2.5-0.5B-Instruct. It fits in
memory on a free Colab T4, and every run takes minutes, not hours.

## Run order
```bash
python 01_build_dataset.py            # writes data/train, val, test, eval_prompts, review_sample.md
python 02_train_lora.py               # baseline run -> runs/baseline/
python 03_before_after.py             # base vs fine-tuned on unseen prompts and test set
python 04_hparam_experiments.py       # six more runs; writes 04_experiments.csv
python 02_train_lora.py --out runs/match --scheduler constant --warmup 0 --lora-dropout 0
python 05_under_the_hood.py           # manual LoRA; compares against runs/match
```

## Files
| File | Purpose |
|---|---|
| `common.py` | Model name, system prompt, JSONL helpers, prompt-completion conversion |
| `01_build_dataset.py` | Builds ~700 validated support replies, stratified split, unseen eval prompts |
| `02_train_lora.py` | SFTTrainer + LoRA (or QLoRA with `--qlora`), logs loss curves, saves adapter |
| `03_before_after.py` | Side-by-side base vs fine-tuned outputs; test-set token-F1 |
| `04_hparam_experiments.py` | Runs one-factor experiments via `02_train_lora.py` and summarizes them |
| `05_under_the_hood.py` | LoRA in plain PyTorch with a manual loop; checks the math and compares curves |

## Dataset: task, format, and limits
- **Task:** customer-support replies for a fictional SaaS product, "Acme Sync". Intents include password
  reset, refunds, export failures, API rate limits, and a scope-refusal class for off-topic questions.
- **Format:** each example is `{"messages": [system, user, assistant]}`. `to_prompt_completion` converts it to
  TRL's conversational prompt-completion format, and TRL applies the model's chat template. The rendered
  template is printed at the start of `02_train_lora.py` so you can check it.
- **Split:** 80/10/10, stratified by intent. Validation and test come from the same generator, so they measure
  in-distribution fit. The 25 eval prompts in `01_build_dataset.py` are hand-written and cover paraphrases,
  new topics, off-topic requests, and tricky inputs. They are the real generalization test.
- **Limit:** templates give consistent style and policy, but the model may learn the phrasing rather than the
  skill. Read `data/review_sample.md`. Consider adding human-written or LLM-paraphrased replies before you
  rely on this.
- **Policy consistency:** replies state specific policies (30-day refunds, 50,000-row export limit, 7-day
  grace period). These are invented for the exercise. Check that your version of the dataset uses your
  product's real rules, or the model will confidently state fake policy.

## LoRA in brief
A frozen weight matrix `W` gets a trainable low-rank update: `W' = W + (alpha / r) * B @ A`, where `A` is
`r x in` and `B` is `out x r`. `B` starts at zero, so training begins from the base model exactly. Only `A` and
`B` are trained, so the adapter is a small fraction of the model. Scaling by `alpha / r` keeps the update size
steady when you change `r`.

**QLoRA** keeps the base weights in 4-bit NF4 and computes in bf16. It saves memory, which matters for larger
models. For this 0.5B model, plain LoRA is enough.

## Loss on completions only
Loss is computed only on the assistant reply. The prompt tokens are masked with `-100`, so the model learns to
answer, not to reproduce the user's message or system prompt.

## Results
Fill in after running.

### Exercise 2: Baseline loss curves
- Final validation loss and test loss:
- Did train and validation loss diverge? At what step, if so?
- Trainable parameters and adapter size:

### Exercise 3: Before vs. after
- Share of in-scope replies that name Acme Sync, base vs fine-tuned:
- Off-topic prompts redirected to Acme Sync, base vs fine-tuned:
- Test-set token-F1, base vs fine-tuned:
- Read `03_before_after.md`. Which unseen prompts did the fine-tuned model handle well? Which did it get wrong, and
  what does that suggest about the training data?
- Did the fine-tuned model invent policies on "Is there a student discount?" or "Does Acme Sync work offline?"
- Did it fall into template phrasing on the paraphrased prompts?

### Exercise 4: Experiments (see 04_experiments.csv)
| Run | Change | Best val loss | Test loss | Train time |
|---|---|---|---|---|
| baseline | rank 16, lr 2e-4, full data | | | |
| rank_4 | rank 4 | | | |
| rank_64 | rank 64 | | | |
| lr_5e-5 | lr 5e-5 | | | |
| lr_1e-3 | lr 1e-3 | | | |
| data_300 | 300 train examples | | | |
| data_100 | 100 train examples | | | |

- Which change had the largest effect on validation loss? Was it the rank, the learning rate, or the data size?
- Did higher rank help? At what point did it stop helping?
- Did the highest learning rate show instability (loss spikes or rising validation loss)?
- How much data was needed before validation loss stopped improving?
- Did a smaller dataset overfit, meaning train loss kept falling while validation loss rose?

### Exercise 5: Under the hood
- Are the LoRA math checks passing?
- Mean relative difference between the manual loop and SFTTrainer:
- If there's a gap, the likely causes are:
  - The two runs shuffle data differently.
  - Tokenization of prompt and completion can differ at the boundary.
  - The trainer's end-of-turn handling may differ by one token.
  - Batch-mean versus token-mean averaging in the eval loss.
