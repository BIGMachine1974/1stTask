"""MCP server that provides knowledge_search as a tool for agents.

This runs as an in-process MCP server via the Claude Agent SDK's custom tools.
Agents can call knowledge_search(query, ...) to retrieve relevant context from
the user's past work stored in ChromaDB.
"""

from backend.knowledge.retriever import KnowledgeRetriever

# Global retriever instance (initialized lazily)
_retriever: KnowledgeRetriever | None = None


def _get_retriever() -> KnowledgeRetriever:
    global _retriever
    if _retriever is None:
        _retriever = KnowledgeRetriever()
    return _retriever


def knowledge_search(
    query: str,
    n_results: int = 5,
    source_type: str | None = None,
    collections: str | None = None,
) -> str:
    """Search the knowledge base for information relevant to a query.

    Use this tool to find context from the user's past work, conversations,
    code, documents, and decisions. Always check the knowledge base before
    answering questions about the user's projects or preferences.

    Args:
        query: What to search for. Be specific and descriptive.
        n_results: Maximum number of results to return (default 5).
        source_type: Filter by source type: "conversation", "code", "document", or "decision".
        collections: Comma-separated collection names to search. Default: all.

    Returns:
        Formatted search results with relevant text and metadata.
    """
    retriever = _get_retriever()

    col_list = [c.strip() for c in collections.split(",")] if collections else None

    results = retriever.search(
        query=query,
        collections=col_list,
        n_results=n_results,
        source_type=source_type,
    )

    if not results:
        return "No relevant results found in the knowledge base."

    formatted = []
    for i, r in enumerate(results, 1):
        meta = r["metadata"]
        source = meta.get("source_file", "unknown")
        stype = meta.get("source_type", "unknown")
        formatted.append(f"--- Result {i} (type: {stype}, source: {source}) ---\n{r['text'][:1500]}")

    return "\n\n".join(formatted)
