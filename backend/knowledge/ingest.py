"""Ingestion pipeline: scan sources, extract, chunk, embed, store in ChromaDB."""

import uuid
from pathlib import Path

import chromadb

from backend.knowledge.chunker import chunk_texts
from backend.knowledge.embedder import Embedder, get_embedder
from backend.knowledge.extractors.chat_transcript import extract_chat_transcript
from backend.knowledge.extractors.code_repo import extract_code_repo
from backend.knowledge.extractors.documents import extract_document
from backend.knowledge.types import Chunk

# Map source_type to ChromaDB collection name
SOURCE_TO_COLLECTION = {
    "conversation": "conversations",
    "code": "code",
    "document": "documents",
    "decision": "decisions",
}

# File extensions and how to extract them
CHAT_EXTENSIONS = {".json"}
DOC_EXTENSIONS = {".md", ".txt", ".rst", ".pdf", ".org"}
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
    ".sh", ".sql", ".yaml", ".yml", ".toml",
}


def ingest_path(
    source_path: str,
    persist_dir: str = "./chromadb_data",
    embedding_backend: str = "local",
    chunk_size: int = 500,
) -> dict:
    """Ingest a file or directory into ChromaDB.

    Args:
        source_path: Path to a file or directory.
        persist_dir: ChromaDB persistence directory.
        embedding_backend: "local" or "voyage".
        chunk_size: Target chunk size in tokens.

    Returns:
        Stats dict with counts of items processed.
    """
    path = Path(source_path)
    embedder = get_embedder(embedding_backend)
    client = chromadb.PersistentClient(path=persist_dir)

    stats = {"files_scanned": 0, "chunks_extracted": 0, "chunks_stored": 0}

    # 1. Extract raw chunks
    raw_chunks: list[Chunk] = []

    if path.is_file():
        raw_chunks.extend(_extract_file(path))
        stats["files_scanned"] = 1
    elif path.is_dir():
        for file_path in _walk_all_files(path):
            extracted = _extract_file(file_path)
            if extracted:
                raw_chunks.extend(extracted)
                stats["files_scanned"] += 1
    else:
        raise ValueError(f"Path does not exist: {source_path}")

    stats["chunks_extracted"] = len(raw_chunks)
    print(f"  Extracted {len(raw_chunks)} chunks from {stats['files_scanned']} files")

    if not raw_chunks:
        return stats

    # 2. Chunk into smaller pieces
    chunks = chunk_texts(raw_chunks, chunk_size=chunk_size)
    print(f"  Split into {len(chunks)} chunks after chunking")

    # 3. Embed and store by collection
    by_collection: dict[str, list[Chunk]] = {}
    for chunk in chunks:
        source_type = chunk.metadata.get("source_type", "document")
        col_name = SOURCE_TO_COLLECTION.get(source_type, "documents")
        by_collection.setdefault(col_name, []).append(chunk)

    for col_name, col_chunks in by_collection.items():
        stored = _store_chunks(client, col_name, col_chunks, embedder)
        stats["chunks_stored"] += stored
        print(f"  Stored {stored} chunks in '{col_name}' collection")

    return stats


def _extract_file(path: Path) -> list[Chunk]:
    """Extract chunks from a single file based on its type."""
    suffix = path.suffix.lower()

    try:
        if suffix in CHAT_EXTENSIONS:
            return extract_chat_transcript(path)
        elif suffix in DOC_EXTENSIONS:
            return extract_document(path)
        elif suffix in CODE_EXTENSIONS:
            return extract_code_repo(path)
        else:
            return extract_document(path)
    except Exception as e:
        print(f"  Warning: failed to extract {path.name}: {e}")
        return []


def _walk_all_files(root: Path):
    """Walk a directory yielding all processable files."""
    skip_dirs = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", "target", "chromadb_data",
    }
    for item in root.rglob("*"):
        if any(skip in item.parts for skip in skip_dirs):
            continue
        if item.is_file() and item.stat().st_size > 0:
            yield item


def _store_chunks(
    client: chromadb.PersistentClient,
    collection_name: str,
    chunks: list[Chunk],
    embedder: Embedder,
) -> int:
    """Embed and store chunks in a ChromaDB collection."""
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c.text for c in chunks]
    metadatas = [c.metadata for c in chunks]
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Embed in batches
    batch_size = 64
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        all_embeddings.extend(embedder.embed(batch))

    # Store in batches (ChromaDB has limits)
    chroma_batch = 5000
    stored = 0
    for i in range(0, len(texts), chroma_batch):
        end = i + chroma_batch
        # Sanitize metadata - ChromaDB only accepts str, int, float, bool
        sanitized = [_sanitize_metadata(m) for m in metadatas[i:end]]
        collection.add(
            ids=ids[i:end],
            documents=texts[i:end],
            embeddings=all_embeddings[i:end],
            metadatas=sanitized,
        )
        stored += len(texts[i:end])

    return stored


def _sanitize_metadata(meta: dict) -> dict:
    """Ensure metadata values are ChromaDB-compatible types."""
    result = {}
    for k, v in meta.items():
        if isinstance(v, (str, int, float, bool)):
            result[k] = v
        else:
            result[k] = str(v)
    return result
