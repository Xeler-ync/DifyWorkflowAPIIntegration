# -*- coding: utf-8 -*-
import os
from gensim.models import Word2Vec

BASE = os.path.dirname(__file__)
MODELS = os.path.join(BASE, "..", "models")

def show_neighbors(model_path, words):
    wv = Word2Vec.load(model_path).wv
    for w in words:
        if w in wv.key_to_index:
            print(f"\nTop neighbors for [{w}]")
            for x, score in wv.most_similar(w, topn=10):
                print(f"  {x}\t{score:.3f}")
        else:
            print(f"\n[{w}] not in vocabulary.")

if __name__ == "__main__":
    words = ["入住", "退房", "押金", "早餐", "停车", "宠物", "发票"]
    show_neighbors(os.path.join(MODELS, "w2v_sg.model"), words)
