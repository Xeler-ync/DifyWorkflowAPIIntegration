# -*- coding: utf-8 -*-
# Visualize selected words in 2D using t-SNE. Saves models/tsne.png.
import os, numpy as np
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

BASE   = os.path.dirname(__file__)
MODELS = os.path.join(BASE, "..", "models")

def main():
    model_path = os.path.join(MODELS, "w2v_sg.model")
    if not os.path.exists(model_path):
        print("Missing w2v_sg.model. Train first: python scripts/train_w2v.py")
        return
    wv = Word2Vec.load(model_path).wv

    vocab = ["入住","退房","延迟","提前","押金","发票","早餐","停车","宠物","加床","健身房","游泳池","洗衣房","充电桩","亲子房","前台","预授权","无烟房","接机"]
    words = [w for w in vocab if w in wv.key_to_index]
    if len(words) < 5:
        print("Too few words in vocab for plotting. Train on larger corpus.")
        return

    X = np.array([wv[w] for w in words])
    Y = TSNE(n_components=2, init="random", learning_rate="auto", perplexity=5).fit_transform(X)

    out_path = os.path.join(MODELS, "tsne.png")
    plt.figure()
    plt.scatter(Y[:,0], Y[:,1])
    for i, w in enumerate(words):
        plt.annotate(w, (Y[i,0], Y[i,1]))
    plt.title("Hotel domain word clusters (t-SNE)")
    plt.savefig(out_path, dpi=180, bbox_inches="tight")
    print("Saved plot:", out_path)

if __name__ == "__main__":
    main()
