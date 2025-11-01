# -*- coding: utf-8 -*-
import os
import numpy as np
from numpy.linalg import norm
from gensim.models import Word2Vec
from utils import sent_embed, load_user_dict

BASE   = os.path.dirname(__file__)
MODELS = os.path.join(BASE, "..", "models")

def cosine(a, b):
    a = a / (norm(a) + 1e-9)
    b = b / (norm(b, axis=1, keepdims=True) + 1e-9)
    return (a @ b.T).ravel()

def main():
    load_user_dict()
    idx_path = os.path.join(MODELS, "faq_index.npz")
    if not os.path.exists(idx_path):
        raise FileNotFoundError("Missing models/faq_index.npz. Run build_retrieval.py first.")

    data = np.load(idx_path, allow_pickle=True)
    faq_ids = data["faq_ids"]
    faq_q   = data["faq_q"]
    faq_a   = data["faq_a"]
    faq_mat = data["faq_mat"]
    dim     = int(data["dim"])
    model_name = str(data["model"])

    wv = Word2Vec.load(os.path.join(MODELS, model_name)).wv

    print("Type a question (Chinese). Example: 可以提前入住吗   (type 'quit' to exit)")
    while True:
        try:
            q = input("\nYour question: ").strip()
        except EOFError:
            break
        if q.lower() in {"quit", "exit"}:
            break
        q_vec = sent_embed(q, wv, dim)
        sims = cosine(q_vec, faq_mat)
        topk = sims.argsort()[::-1][:5]
        print("Top-5:")
        for i in topk:
            print(f"- [{faq_ids[i]}] {faq_q[i]}  (score={sims[i]:.3f})")
            print(f"  → {faq_a[i]}")

if __name__ == "__main__":
    main()
