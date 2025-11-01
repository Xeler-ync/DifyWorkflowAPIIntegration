# -*- coding: utf-8 -*-
# Optional: build a FAISS index for FAQ sentence embeddings.
# Requires: pip install faiss-cpu
# Saves: models/faq_faiss.index and models/faq_faiss_meta.npz

import os, numpy as np, importlib
from gensim.models import Word2Vec
from utils import sent_embed, load_user_dict

BASE   = os.path.dirname(__file__)
DATA   = os.path.join(BASE, "..", "data")
MODELS = os.path.join(BASE, "..", "models")

def main():
    if importlib.util.find_spec("faiss") is None:
        print("faiss not installed. Run: pip install faiss-cpu  (optional).")
        return
    import faiss

    load_user_dict()
    model_path = os.path.join(MODELS, "w2v_sg.model")
    if not os.path.exists(model_path):
        print("Missing model. Train first: python scripts/train_w2v.py")
        return
    wv = Word2Vec.load(model_path).wv
    dim = wv.vector_size

    import pandas as pd
    faq_path = os.path.join(DATA, "faq.csv")
    if not os.path.exists(faq_path):
        print("Missing data/faq.csv")
        return
    faq = pd.read_csv(faq_path)

    mats = [sent_embed(str(q), wv, dim) for q in faq["question"]]
    mat = np.vstack(mats).astype("float32")

    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-9
    mat_norm = mat / norms

    index = faiss.IndexFlatIP(dim)
    index.add(mat_norm)

    faiss.write_index(index, os.path.join(MODELS, "faq_faiss.index"))
    np.savez(os.path.join(MODELS, "faq_faiss_meta.npz"),
             faq_ids=faq["id"].values,
             faq_q=faq["question"].values,
             faq_a=faq["answer"].values)
    print("Built FAISS index. Files saved in models/.")

if __name__ == "__main__":
    main()
