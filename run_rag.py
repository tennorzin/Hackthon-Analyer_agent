import os
import json
from ingest.parse_docx import extract_text_from_docx
from ingest.chunker import chunk_text
from retrieval.bm25_retrieval import build_bm25_index, retrieve_bm25

# 1) Load and chunk SOW docs
base_dir = "data"
all_chunks = []
for fname in os.listdir(base_dir):
    if fname.endswith(".docx"):
        text = extract_text_from_docx(os.path.join(base_dir, fname))
        for j, chunk in enumerate(chunk_text(text)):
            all_chunks.append({
                "sow_id": fname,
                "chunk_id": f"{fname}_{j}",
                "content": chunk
            })

# 2) Build the BM25 index
corpus = [c["content"] for c in all_chunks]
bm25, tokenized = build_bm25_index(corpus)

# 3) Run retrieval on a sample query
query = "data validation responsibilities in migration"
results = retrieve_bm25(bm25, tokenized, query, top_k=5)

# 4) Map indexed results back to chunk content
formatted = []
for r in results:
    doc = all_chunks[r["doc_index"]]
    formatted.append({
        "sow_id": doc["sow_id"],
        "chunk_id": doc["chunk_id"],
        "content": doc["content"],
        "score": r["score"]
    })

# 5) Create final JSON output
output = {
    "query": query,
    "retrieved_chunks": formatted
}

# 6) Write results to file
output_path = "rag_retrieval_output.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Results written to {output_path}")