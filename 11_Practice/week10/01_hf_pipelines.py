"""
Exercise 1: Hugging Face Pipelines
Runs pretrained pipelines for sentiment, NER, question answering, and summarization on
hand-written inputs chosen to expose both strengths and failure modes. Models are pinned
so results are reproducible.

Usage: python 01_hf_pipelines.py
"""
import json
import torch
from transformers import pipeline

DEVICE = 0 if torch.cuda.is_available() else -1
MODELS = {
    "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
    "ner": "dslim/bert-base-NER",
    "qa": "distilbert-base-cased-distilled-squad",
    "summarization": "sshleifer/distilbart-cnn-12-6",
}

SENTIMENT_CASES = [
    ("easy positive", "This movie was an absolute masterpiece, I loved every minute."),
    ("negation", "The film was not without its charms."),
    ("mild positive", "Not bad at all, actually quite enjoyable."),
    ("sarcasm", "Oh great, another two hours of my life I'll never get back."),
    ("mixed", "The acting was superb, but the plot was a complete mess."),
    ("domain shift", "The new model's latency is lower but its accuracy regressed badly."),
]

NER_CASES = [
    ("clean news", "Satya Nadella announced that Microsoft would open a new office in Hyderabad."),
    ("lowercase", "tim cook visited apple park in cupertino last week."),
    ("ambiguous", "Jordan played basketball in Jordan before moving to Amazon."),
    ("unusual entity", "Ahmedabad's Sabarmati Riverfront draws visitors from across Gujarat."),
]

QA_CONTEXT = ("The Eiffel Tower was designed by the engineering firm of Gustave Eiffel and "
              "completed in 1889 as the centerpiece of the World's Fair in Paris. It stood as "
              "the tallest man-made structure in the world for 41 years.")
QA_QUESTIONS = [
    ("answerable", "When was the Eiffel Tower completed?"),
    ("answerable", "Who designed it?"),
    ("not in context", "How tall is the Eiffel Tower?"),
    ("unanswerable", "What is the population of Paris?"),
]

SUMMARY_TEXT = (
    "Transformer models replaced recurrent networks as the default architecture for most "
    "natural language tasks after 2017. Their self-attention mechanism lets every token "
    "attend to every other token in a single step, which makes them easier to parallelize "
    "during training and better at capturing long-range dependencies. Pretraining on large "
    "unlabeled corpora followed by task-specific fine-tuning turned out to work especially "
    "well, and it allowed small teams to reach strong results with modest labeled datasets. "
    "The trade-off is cost: attention scales quadratically with sequence length, and large "
    "models need substantial memory and compute, which has pushed interest toward smaller, "
    "distilled variants for production use."
)


if __name__ == "__main__":
    results = {}

    print("=== Sentiment (distilbert-sst2) ===")
    clf = pipeline("sentiment-analysis", model=MODELS["sentiment"], device=DEVICE)
    results["sentiment"] = []
    for tag, text in SENTIMENT_CASES:
        out = clf(text)[0]
        results["sentiment"].append({"case": tag, "text": text, **out})
        print(f"[{tag:<14}] {out['label']:<8} {out['score']:.3f}  | {text}")
    del clf

    print("\n=== Named entity recognition (bert-base-NER, aggregated spans) ===")
    ner = pipeline("ner", model=MODELS["ner"], aggregation_strategy="simple", device=DEVICE)
    results["ner"] = []
    for tag, text in NER_CASES:
        ents = [{"word": e["word"], "group": e["entity_group"], "score": round(float(e["score"]), 3)}
                for e in ner(text)]
        results["ner"].append({"case": tag, "text": text, "entities": ents})
        print(f"[{tag}] {text}")
        for e in ents:
            print(f"    {e['word']:<22} {e['group']:<6} {e['score']:.3f}")
    del ner

    print("\n=== Question answering (distilbert-squad) ===")
    qa = pipeline("question-answering", model=MODELS["qa"], device=DEVICE)
    results["qa"] = []
    for tag, q in QA_QUESTIONS:
        out = qa(question=q, context=QA_CONTEXT)
        results["qa"].append({"case": tag, "question": q, "answer": out["answer"],
                              "score": round(float(out["score"]), 3)})
        print(f"[{tag:<14}] Q: {q}\n                 A: '{out['answer']}'  (score {out['score']:.3f})")
    del qa

    print("\n=== Summarization (distilbart-cnn) ===")
    summ = pipeline("summarization", model=MODELS["summarization"], device=DEVICE)
    out = summ(SUMMARY_TEXT, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
    results["summarization"] = {"summary": out, "input_words": len(SUMMARY_TEXT.split()),
                                "summary_words": len(out.split())}
    print(out)
    print(f"Input {len(SUMMARY_TEXT.split())} words -> summary {len(out.split())} words")

    with open("01_pipeline_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved 01_pipeline_results.json. Record where each task succeeded or failed in README.md.")
