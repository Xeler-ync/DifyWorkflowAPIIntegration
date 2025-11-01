# -*- coding: utf-8 -*-
import os
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")
MODELS = os.path.join(BASE, "..", "models")

def read_tokenized(path):
    sents = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            toks = ln.strip().split()
            if toks:
                sents.append(toks)
    return sents

def main():
    os.makedirs(MODELS, exist_ok=True)
    tokenized_path = os.path.join(DATA, "corpus_tokenized.txt")
    if not os.path.exists(tokenized_path):
        raise FileNotFoundError("Missing data/corpus_tokenized.txt. Run prep_tokenize.py first.")

    sents = read_tokenized(tokenized_path)

    # Word2Vec Skip-gram & CBOW
    w2v_sg = Word2Vec(
        sents, vector_size=200, window=5, min_count=2,
        sg=1, negative=10, epochs=10, workers=4
    )
    w2v_cb = Word2Vec(
        sents, vector_size=200, window=5, min_count=2,
        sg=0, negative=10, epochs=10, workers=4
    )
    w2v_sg.save(os.path.join(MODELS, "w2v_sg.model"))
    w2v_cb.save(os.path.join(MODELS, "w2v_cb.model"))
    print("Saved:", os.path.join(MODELS, "w2v_sg.model"))
    print("Saved:", os.path.join(MODELS, "w2v_cb.model"))

    # Optional: FastText
    ft = FastText(
        sents, vector_size=200, window=5, min_count=2,
        sg=1, epochs=10, workers=4
    )
    ft.save(os.path.join(MODELS, "fasttext.model"))
    print("Saved:", os.path.join(MODELS, "fasttext.model"))

if __name__ == "__main__":
    main()
