from rank_bm25 import BM25Okapi
import re

# Simple tokenizer to split text into terms
def tokenize(text):
    # lowercase + split on non-letters
    return re.findall(r"\w+", text.lower())

def build_bm25_index(corpus):
    """
    corpus: list of strings (each doc or chunk)
    returns BM25 model, tokenized corpus
    """
    tokenized = [tokenize(doc) for doc in corpus]
    bm25 = BM25Okapi(tokenized)
    return bm25, tokenized

def retrieve_bm25(bm25, tokenized_corpus, query, top_k=5):
    """
    bm25: BM25Okapi instance
    tokenized_corpus: pre-tokenized corpus list
    query: raw query text
    """
    q_tokens = tokenize(query)
    scores = bm25.get_scores(q_tokens)  # scores for each doc
    # sort by score descending
    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )
    top_results = ranked[:top_k]
    
    results = []
    for idx, score in top_results:
        results.append({
            "doc_index": idx,
            "score": float(score)
        })
    return results