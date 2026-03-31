"""Query ChromaDB for relevant knowledge chunks."""

import chromadb

from backend.knowledge.embedder import Embedder, get_embedder

# Collection names matching our source types
COLLECTIONS = ["documents", "conversations", "code", "decisions"]


class KnowledgeRetriever:
    """Retrieve relevant chunks from ChromaDB."""

    def __init__(self, persist_dir: str = "./chromadb_data", embedder: Embedder | None = None):
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._embedder = embedder or get_embedder()

    def search(
        self,
        query: str,
        collections: list[str] | None = None,
        n_results: int = 10,
        source_type: str | None = None,
    ) -> list[dict]:
        """Search for chunks relevant to the query.

        Args:
            query: The search query.
            collections: Which collections to search (default: all).
            n_results: Max results per collection.
            source_type: Filter by source_type metadata.

        Returns:
            List of dicts with "text", "metadata", "distance" keys, sorted by relevance.
        """
        target_collections = collections or COLLECTIONS
        query_embedding = self._embedder.embed([query])[0]

        all_results = []
        for col_name in target_collections:
            try:
                collection = self._client.get_collection(col_name)
            except Exception:
                continue

            where_filter = {"source_type": source_type} if source_type else None
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter,
            )

            if results["documents"] and results["documents"][0]:
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                ):
                    all_results.append({
                        "text": doc,
                        "metadata": meta,
                        "distance": dist,
                        "collection": col_name,
                    })

        # Sort by distance (lower = more relevant)
        all_results.sort(key=lambda x: x["distance"])
        return all_results[:n_results]
