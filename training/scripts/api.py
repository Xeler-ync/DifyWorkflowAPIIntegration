# -*- coding: utf-8 -*-
import os
import json
import sys
from typing import Optional
import numpy as np
from numpy.linalg import norm
from multiprocessing import Process, Pipe

# Local imports
from .utils import load_user_dict, sent_embed

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")
MODELS = os.path.join(BASE, "..", "models")

# Globals loaded at startup
WV = None  # keyed vectors object (gensim .wv)
FAQ_IDS = None  # np.ndarray
FAQ_Q = None  # np.ndarray of str
FAQ_A = None  # np.ndarray of str
FAQ_MAT = None  # np.ndarray (N, D), normalized


def _normalize_rows(mat: np.ndarray) -> np.ndarray:
    denom = np.maximum(norm(mat, axis=1, keepdims=True), 1e-9)
    return mat / denom


def _cosine_search(q_vec: np.ndarray, k: int = 5):
    if q_vec.ndim == 1:
        q_vec = q_vec.reshape(1, -1)
    qv = q_vec / (norm(q_vec) + 1e-9)
    sims = (qv @ FAQ_MAT.T).ravel()  # inner product on normalized vectors == cosine
    idx = sims.argsort()[::-1][:k]
    return idx, sims


def _load_all():
    """Load user dict, model, and FAQ index (build if missing)."""
    global WV, FAQ_IDS, FAQ_Q, FAQ_A, FAQ_MAT
    load_user_dict()

    # 1) Load embedding model (prefer Word2Vec Skip-gram, fallback FastText)
    from gensim.models import Word2Vec
    from gensim.models.fasttext import FastText

    w2v_path = os.path.join(MODELS, "w2v_sg.model")
    ft_path = os.path.join(MODELS, "fasttext.model")

    if os.path.exists(w2v_path):
        WV = Word2Vec.load(w2v_path).wv
        dim = WV.vector_size
        model_name = "w2v_sg.model"
    elif os.path.exists(ft_path):
        WV = FastText.load(ft_path).wv
        dim = WV.vector_size
        model_name = "fasttext.model"
    else:
        raise RuntimeError(
            "No embedding model found. Run 'python scripts/train_w2v.py' first."
        )

    # 2) Load FAQ index if exists, else build from data/faq.csv
    idx_path = os.path.join(MODELS, "faq_index.npz")
    if os.path.exists(idx_path):
        data = np.load(idx_path, allow_pickle=True)
        FAQ_IDS = data["faq_ids"]
        FAQ_Q = data["faq_q"]
        FAQ_A = data["faq_a"]
        FAQ_MAT = data["faq_mat"].astype("float32")
        # Normalize once for cosine
        FAQ_MAT[:] = _normalize_rows(FAQ_MAT)
    else:
        import pandas as pd

        faq_path = os.path.join(DATA, "..", "data", "faq.csv")  # normalize path
        faq_path = os.path.abspath(faq_path)
        if not os.path.exists(faq_path):
            raise RuntimeError("Missing data/faq.csv. Please create it and try again.")
        faq = pd.read_csv(faq_path)
        FAQ_IDS = faq["id"].values
        FAQ_Q = faq["question"].values
        FAQ_A = faq["answer"].values
        mats = []
        for q in FAQ_Q:
            mats.append(sent_embed(str(q), WV, dim))
        FAQ_MAT = _normalize_rows(np.vstack(mats).astype("float32"))

    print(
        f"[startup] Loaded model={model_name}, dim={WV.vector_size}, FAQs={len(FAQ_Q)}"
    )


def _handle_search(data):
    q = data.get("q")
    k = data.get("k", 5)
    vec = sent_embed(q, WV, WV.vector_size)
    idx, sims = _cosine_search(vec, k=k)
    results = []
    for i in idx:
        results.append(
            {
                "id": int(FAQ_IDS[i]),
                "question": str(FAQ_Q[i]),
                "answer": str(FAQ_A[i]),
                "score": float((vec / (norm(vec) + 1e-9) @ FAQ_MAT[i])),
            }
        )
    return {"q": q, "k": k, "results": results, "request_id": data["request_id"]}


def _handle_ping():
    return {"ok": True, "msg": "pong"}


def _process_message(conn):
    while True:
        try:
            if conn.closed:
                break
            data = conn.recv()
            if not data:
                break

            msg_type = data.get("type")
            if msg_type == "ping":
                response = _handle_ping()
            elif msg_type == "search":
                response = _handle_search(data)
            else:
                response = {"error": "Unknown message type"}

            conn.send(response)
        except (ConnectionError, EOFError):
            break
        except Exception as e:
            print(f"Error in search process: {e}")
            conn.send({"error": str(e)})
            break


def start_search_process():
    """启动搜索进程的函数，返回管道连接对象"""
    import multiprocessing
    import platform

    # 根据操作系统设置不同的启动方式
    if platform.system() == "Windows":
        multiprocessing.set_start_method("spawn", force=True)
    else:
        multiprocessing.set_start_method("fork", force=True)

    parent_conn, child_conn = multiprocessing.Pipe()

    def run():
        try:
            _load_all()
            _process_message(child_conn)
        except Exception as e:
            print(f"Error in search process: {e}")
        finally:
            child_conn.close()

    p = multiprocessing.Process(target=run)
    p.daemon = True  # 设置为守护进程
    p.start()

    # 关闭子进程中的连接
    child_conn.close()

    return parent_conn


def start(child_conn):
    """启动，使用传入的管道连接对象"""
    try:
        _load_all()
        _process_message(child_conn)
    except Exception as e:
        print(f"Error in search process: {e}")
    finally:
        child_conn.close()
