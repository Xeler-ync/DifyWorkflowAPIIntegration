# -*- coding: utf-8 -*-
import os
from utils import load_user_dict, read_corpus_lines, tokenize_zh

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")

def main():
    load_user_dict()
    corpus_path = os.path.join(DATA, "corpus.txt")
    out_path = os.path.join(DATA, "corpus_tokenized.txt")

    lines = read_corpus_lines(corpus_path)
    tokenized = [tokenize_zh(ln) for ln in lines]

    with open(out_path, "w", encoding="utf-8") as f:
        for toks in tokenized:
            f.write(" ".join(toks) + "\n")

    print(f"Done. Wrote tokenized sentences to: {out_path}")
    for i in range(min(5, len(tokenized))):
        print(i, "→", tokenized[i])

if __name__ == "__main__":
    main()
