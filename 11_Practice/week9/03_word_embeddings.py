"""
Exercise 3: Word Embeddings Exploration
Trains Word2Vec (gensim) on the IMDB reviews, explores nearest neighbors and analogies,
and visualizes the embedding space in 2D with PCA and t-SNE.

Pass --glove to use pretrained GloVe (gensim downloads ~130MB on first run) instead.
Usage: python 03_word_embeddings.py data/IMDB\ Dataset.csv [--glove]
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from text_pipeline import TextCleaner, load_imdb

args = [a for a in sys.argv[1:] if not a.startswith("--")]
PATH = args[0] if args else "data/IMDB Dataset.csv"
USE_GLOVE = "--glove" in sys.argv

# Word2Vec learns from context, so keep negations and common words (remove_stopwords=False).
PAIRS = [
    ("good", "better", "bad"),        # expect "worse"
    ("man", "king", "woman"),         # expect "queen" (corpus-dependent)
    ("actor", "actress", "director"), # gender-related pairs
]


def analogy(wv, a, b, c, topn=3):
    """a : b :: c : ?  via vector arithmetic b - a + c."""
    return wv.most_similar(positive=[b, c], negative=[a], topn=topn)


if __name__ == "__main__":
    if USE_GLOVE:
        import gensim.downloader as api
        wv = api.load("glove-wiki-gigaword-100")   # KeyedVectors
        print("Loaded pretrained GloVe-100 (Wikipedia + Gigaword, 400k vocab)")
    else:
        X_tr, _, _, _ = load_imdb(PATH)
        cleaner = TextCleaner(remove_stopwords=False, normalize=None)
        sentences = [d.split() for d in cleaner.transform(X_tr)]
        model = Word2Vec(sentences, vector_size=100, window=5, min_count=5,
                         sg=1, workers=4, epochs=10, seed=42)
        model.save("word2vec_imdb.model")
        wv = model.wv
        print(f"Trained Word2Vec: vocab={len(wv)}, dim={wv.vector_size}")

    print("\n== Nearest neighbors (cosine) ==")
    for w in ["good", "terrible", "actor", "boring", "funny"]:
        if w in wv:
            nbrs = ", ".join(f"{n}({s:.2f})" for n, s in wv.most_similar(w, topn=6))
            print(f"  {w:<10} -> {nbrs}")
        else:
            print(f"  {w:<10} not in vocabulary")

    print("\n== Analogies: a : b :: c : ? ==")
    for a, b, c in PAIRS:
        if all(w in wv for w in (a, b, c)):
            res = analogy(wv, a, b, c)
            print(f"  {a}:{b} :: {c}:? -> " + ", ".join(f"{w}({s:.2f})" for w, s in res))
        else:
            print(f"  skipped {a}:{b} :: {c}:? (missing word in vocabulary)")
    print("Analogies work best with a large general corpus like GloVe. "
          "A movie-review corpus has weaker, domain-specific structure.")

    # Visualize the 300 most frequent words in 2D.
    words = [w for w in wv.index_to_key[:300] if w.isalpha()][:250]
    vecs = np.array([wv[w] for w in words])
    pca_xy = PCA(n_components=2, random_state=42).fit_transform(vecs)
    tsne_xy = TSNE(n_components=2, perplexity=30, random_state=42, init="pca",
                   learning_rate="auto").fit_transform(vecs)

    fig, ax = plt.subplots(1, 2, figsize=(18, 9))
    for a_, xy, title in [(ax[0], pca_xy, "PCA"), (ax[1], tsne_xy, "t-SNE")]:
        a_.scatter(xy[:, 0], xy[:, 1], s=8, alpha=0.4)
        for w, (x, y) in zip(words[:150], xy[:150]):
            a_.annotate(w, (x, y), fontsize=8)
        a_.set_title(f"{title} of word embeddings (top words)")
        a_.grid(alpha=0.2)
    plt.tight_layout(); plt.savefig("03_embedding_space.png", dpi=120)
    print("\nSaved 03_embedding_space.png")
