# -*- coding: utf-8 -*-
# Optional FAISS console search.
import os, numpy as np, importlib
from gensim.models import Word2Vec
from utils import sent_embed, load_user_dict

BASE   = os.path.dirname(__file__)
MODELS = os.path.join(BASE, "..", "models")

def main():
    if importlib.util.find_spec("faiss") is None:
        print("faiss not installed. Run: pip install faiss-cpu  (optional).")
        return
    import faiss

    load_user_dict()
    idx_path = os.path.join(MODELS, "faq_faiss.index")
    meta_path = os.path.join(MODELS, "faq_faiss_meta.npz")
    if not (os.path.exists(idx_path) and os.path.exists(meta_path)):
        print("Missing FAISS index/meta. Build first: python scripts/build_retrieval_faiss.py")
        return

    data = np.load(meta_path, allow_pickle=True)
    faq_ids = data["faq_ids"]
    faq_q   = data["faq_q"]
    faq_a   = data["faq_a"]

    model_path = os.path.join(MODELS, "w2v_sg.model")
    wv = Word2Vec.load(model_path).wv
    dim = wv.vector_size

    index = faiss.read_index(idx_path)

    print("FAISS search ready. Type Chinese question (or 'quit')")
    while True:
        q = input("\nYour question: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        v = sent_embed(q, wv, dim).astype("float32")
        v = v / (np.linalg.norm(v) + 1e-9)
        D, I = index.search(v.reshape(1, -1), 5)
        for i, d in zip(I[0], D[0]):
            print(f"- [{faq_ids[i]}] {faq_q[i]}  (score={float(d):.3f})")
            print(f"  → {faq_a[i]}")

if __name__ == "__main__":
    main()
