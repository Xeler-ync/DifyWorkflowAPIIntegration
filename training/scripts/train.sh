#!/bin/bash

# Clean & tokenize corpus (reads data/corpus.txt, writes data/corpus_tokenized.txt)
python scripts/prep_tokenize.py

# Train Word2Vec (and FastText) -> models/*.model
python scripts/train_w2v.py

# Build FAQ vectors -> models/faq_index.npz
python scripts/build_retrieval.py
