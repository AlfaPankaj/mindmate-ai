import chromadb
from chromadb.utils import embedding_functions
import os

class VectorMemory:
    def __init__(self):
        # Use local storage for the prototype
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Using a simple default embedding function for the prototype
        # In production, use OpenAI or sentence-transformers
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="user_memories",
            embedding_function=self.ef
        )

    def add_memory(self, user_id: str, text: str, metadata: dict):
        self.collection.add(
            documents=[text],
            metadatas=[{**metadata, "user_id": user_id}],
            ids=[f"{user_id}_{os.urandom(4).hex()}"]
        )

    def search_memories(self, user_id: str, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id}
        )
        return results

vector_memory = VectorMemory()
