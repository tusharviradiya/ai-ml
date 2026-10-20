"""Shared constants and JSONL helpers for week 11."""
import json

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"   # small instruct model with a standard chat template
SYSTEM_PROMPT = ("You are the support assistant for Acme Sync. Answer concisely and politely. "
                 "If a question is unrelated to Acme Sync, say so and offer to help with Acme Sync questions.")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def to_prompt_completion(record):
    """
    Convert {"messages": [system, user, assistant]} into TRL's conversational prompt-completion
    format. TRL then applies the model's chat template and computes loss only on the completion.
    """
    msgs = record["messages"]
    return {"prompt": msgs[:-1], "completion": [msgs[-1]]}
