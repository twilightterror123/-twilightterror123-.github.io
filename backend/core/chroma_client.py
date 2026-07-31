import chromadb
from chromadb.config import Settings as ChromaSettings
from core.config import settings

chroma_client = chromadb.HttpClient(
    host=settings.CHROMA_URL.replace("http://", "").split(":")[0],
    port=int(settings.CHROMA_URL.split(":")[-1]) if ":" in settings.CHROMA_URL else 8000,
    settings=ChromaSettings(anonymized_telemetry=False)
)
