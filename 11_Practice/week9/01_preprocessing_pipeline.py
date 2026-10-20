"""
Exercise 1: Text Preprocessing Pipeline
Walks through cleaning and tokenization step by step on real reviews, then compares
stemming and lemmatization on the same text: vocabulary size, examples where they
disagree, and speed.

Usage: python 01_preprocessing_pipeline.py data/IMDB\ Dataset.csv
"""
import sys
import time
import pandas as pd
from text_pipeline import (clean_text, tokenize, STOP, TextCleaner,
                           load_imdb, get_lemmatizer)
from nltk.stem import PorterStemmer

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/IMDB Dataset.csv"

if __name__ == "__main__":
    X_tr, _, _, _ = load_imdb(PATH)
    sample = X_tr[:3000]
    raw = sample[0]
    print("RAW:", raw[:300], "...\n")

    # Step-by-step on one review, so you can see what each stage does.
    cleaned = clean_text(raw)
    tokens = tokenize(cleaned)
    no_stop = [t for t in tokens if t not in STOP]
    print("CLEANED:", cleaned[:300], "...")
    print("TOKENS (first 25):", tokens[:25])
    print("AFTER STOPWORDS (first 25):", no_stop[:25])
    print(f"Counts: raw tokens={len(tokens)}, after stopword removal={len(no_stop)}\n")

    # Stemming vs lemmatization on the same tokens.
    stemmer = PorterStemmer()
    lemmatizer = get_lemmatizer()
    probe = ["movies", "running", "better", "studies", "happily", "flies",
             "went", "dogs", "waiting", "was", "beautifully", "worst"]
    print(f"{'word':<12}{'stem':<12}{'lemma (noun)':<14}")
    for w in probe:
        print(f"{w:<12}{stemmer.stem(w):<12}{lemmatizer.lemmatize(w):<14}")
    print("\nNote: lemmatize() assumes noun POS unless you pass pos='v' or 'a'. "
          "'went' stays 'went' and 'better' stays 'better'; a POS tagger would fix that.\n")

    # Compare the two normalizers on the same sample of reviews.
    results = {}
    for mode in [None, "stem", "lemma"]:
        cleaner = TextCleaner(normalize=mode)
        t0 = time.time()
        docs = cleaner.transform(sample)
        elapsed = time.time() - t0
        vocab = {t for d in docs for t in d.split()}
        total = sum(len(d.split()) for d in docs)
        results[str(mode)] = {"vocab": len(vocab), "tokens": total, "seconds": round(elapsed, 2)}
    print("Same 3000 reviews under each normalizer:")
    print(pd.DataFrame(results).T)

    # Words that stemming merges but lemmatization keeps apart, and vice versa.
    stem_vocab = {t for d in TextCleaner(normalize="stem").transform(sample) for t in d.split()}
    lem_vocab = {t for d in TextCleaner(normalize="lemma").transform(sample) for t in d.split()}
    raw_vocab = {t for d in TextCleaner(normalize=None).transform(sample) for t in d.split()}
    examples = [w for w in sorted(raw_vocab) if len(w) > 5][:200]
    odd = [(w, stemmer.stem(w), lemmatizer.lemmatize(w)) for w in examples
           if stemmer.stem(w) != lemmatizer.lemmatize(w)][:12]
    print("\nWords where stem and lemma differ:")
    for w, s, l in odd:
        print(f"  {w:<15} stem={s:<12} lemma={l}")

    print("\nReusable: TextCleaner(normalize='lemma') plugs into any sklearn Pipeline.")
    print(f"Stem vocab={len(stem_vocab)}, lemma vocab={len(lem_vocab)}, raw vocab={len(raw_vocab)}")
