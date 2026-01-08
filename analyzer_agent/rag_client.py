from langchain_community.vectorstores import FAISS
from .dummy_embeddings import DummyEmbeddings

class RAGClient:
    def __init__(self, faiss_path: str):
        embeddings = DummyEmbeddings()
        # allow loading pickle from your own FAISS index
        self.vectorstore = FAISS.load_local(
            faiss_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def fetch_relevant_docs(self, query: str, k: int = 5):
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
