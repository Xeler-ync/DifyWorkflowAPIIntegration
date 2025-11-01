# -*- coding: utf-8 -*-
import os
import re
from typing import List
import jieba

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")

def load_user_dict():
    """
    Load user_dict.txt and add common hotel-domain phrases.
    """
    user_dict_path = os.path.join(DATA, "user_dict.txt")
    if os.path.exists(user_dict_path):
        jieba.load_userdict(user_dict_path)
    for w in ["延迟退房", "提前入住", "自助早餐", "押金", "发票抬头", "预授权", "无烟房", "亲子房", "加床", "前台", "预授权"]:
        jieba.add_word(w)

def to_half_width(s: str) -> str:
    out = []
    for ch in s:
        code = ord(ch)
        if code == 0x3000:
            code = 32
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        out.append(chr(code))
    return "".join(out)

def normalize(text: str) -> str:
    text = to_half_width(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\u4e00-\u9fa5a-z0-9 ]+", " ", text)
    return text.strip()

def tokenize_zh(sent: str) -> List[str]:
    sent = normalize(sent)
    toks = [w.strip() for w in jieba.lcut(sent) if w.strip()]
    return toks

def sent_embed(text: str, wv, dim: int = 200):
    toks = tokenize_zh(text)
    vecs = [wv[w] for w in toks if w in wv.key_to_index]
    import numpy as np
    if not vecs:
        return np.zeros(dim, dtype="float32")
    return (sum(vecs) / len(vecs)).astype("float32")

def read_corpus_lines(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    return lines
