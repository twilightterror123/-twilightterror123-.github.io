from typing import List
import uuid
from core.chroma_client import chroma_client
from ai.ollama_client import OllamaClient

class RagService:
    def __init__(self, chroma, ollama: OllamaClient):
        self.chroma = chroma
        self.ollama = ollama

    async def retrieve(self, query: str, user_id: str, top_k: int = 5) -> List[str]:
        embedding = await self.ollama.embed(query)
        collection = self.chroma.get_or_create_collection(f"user_{user_id}")
        results = collection.query(query_embeddings=[embedding], n_results=top_k, include=["documents"])
        docs = results.get("documents", [[]])[0]
        return [doc for doc in docs if doc]

    async def add_document(self, user_id: str, content: str, metadata: dict = None):
        embedding = await self.ollama.embed(content)
        collection = self.chroma.get_or_create_collection(f"user_{user_id}")
        collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[str(uuid.uuid4())]
        )
