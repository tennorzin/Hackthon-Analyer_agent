from typing import List
from langchain.embeddings.base import Embeddings

class DummyEmbeddings(Embeddings):
    """
    A fake embedding class for testing FAISS locally without OpenAI API keys.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Return a fixed-size vector of zeros for each document
        return [[0.0] * 1536 for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [0.0] * 1536

    # Make it callable (required by LangChain FAISS)
    def __call__(self, text: str) -> List[float]:
        return self.embed_query(text)
