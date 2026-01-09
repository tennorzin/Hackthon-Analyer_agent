import faiss
import numpy as np

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    faiss.normalize_L2(embeddings)  # for cosine similarity
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index