# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from utils import sent_embed, load_user_dict

BASE   = os.path.dirname(__file__)
DATA   = os.path.join(BASE, "..", "data")
MODELS = os.path.join(BASE, "..", "models")

def main():
    load_user_dict()
    model_path = os.path.join(MODELS, "w2v_sg.model")
    if not os.path.exists(model_path):
        raise FileNotFoundError("Missing w2v_sg.model. Run train_w2v.py first.")

    wv = Word2Vec.load(model_path).wv

    faq_path = os.path.join(DATA, "faq.csv")
    if not os.path.exists(faq_path):
        raise FileNotFoundError("Missing data/faq.csv.")

    faq = pd.read_csv(faq_path)  # columns: id,question,answer
    dim = wv.vector_size

    mats = []
    for q in faq["question"]:
        mats.append(sent_embed(str(q), wv, dim))
    faq_mat = np.vstack(mats).astype("float32")  # N x D

    np.savez(os.path.join(MODELS, "faq_index.npz"),
             faq_ids=faq["id"].values,
             faq_q=faq["question"].values,
             faq_a=faq["answer"].values,
             faq_mat=faq_mat,
             model="w2v_sg.model",
             dim=np.int32(dim))
    print("Built retrieval index →", os.path.join(MODELS, "faq_index.npz"))

if __name__ == "__main__":
    main()
