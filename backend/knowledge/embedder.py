"""Generate embeddings for text chunks.

Supports two backends:
1. Anthropic Voyage AI (voyage-3-large) — high quality, requires API key
2. Local sentence-transformers — free, runs locally
"""

import os
from typing import Protocol

from backend.knowledge.types import Chunk


class Embedder(Protocol):
    """Interface for embedding backends."""

    def embed(self, texts: list[str]) -> list[list[float]]: ...

    @property
    def dimension(self) -> int: ...


class VoyageEmbedder:
    """Embeddings via Anthropic's Voyage AI API."""

    DIMENSION = 1024
    MODEL = "voyage-3-large"
    BATCH_SIZE = 128

    def __init__(self, api_key: str | None = None):
        try:
            import voyageai
        except ImportError:
            raise ImportError("Install voyageai: pip install voyageai")
        self._client = voyageai.Client(api_key=api_key or os.environ.get("VOYAGE_API_KEY"))

    @property
    def dimension(self) -> int:
        return self.DIMENSION

    def embed(self, texts: list[str]) -> list[list[float]]:
        all_embeddings = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i : i + self.BATCH_SIZE]
            result = self._client.embed(batch, model=self.MODEL)
            all_embeddings.extend(result.embeddings)
        return all_embeddings


class LocalEmbedder:
    """Embeddings via sentence-transformers (runs locally, no API key needed)."""

    DIMENSION = 768
    MODEL = "all-MiniLM-L6-v2"

    def __init__(self, model_name: str | None = None):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError("Install sentence-transformers: pip install sentence-transformers")
        self._model = SentenceTransformer(model_name or self.MODEL)
        self.DIMENSION = self._model.get_sentence_embedding_dimension()

    @property
    def dimension(self) -> int:
        return self.DIMENSION

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = self._model.encode(texts, show_progress_bar=True)
        return [e.tolist() for e in embeddings]


def get_embedder(backend: str = "local") -> Embedder:
    """Get an embedder instance.

    Args:
        backend: "voyage" for Voyage AI, "local" for sentence-transformers.
    """
    if backend == "voyage":
        return VoyageEmbedder()
    return LocalEmbedder()
