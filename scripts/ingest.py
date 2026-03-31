#!/usr/bin/env python3
"""CLI script to ingest files and directories into the knowledge base.

Usage:
    python scripts/ingest.py /path/to/your/data
    python scripts/ingest.py /path/to/chat-export.json
    python scripts/ingest.py /path/to/code-repo --backend voyage
    python scripts/ingest.py /path/to/docs --chunk-size 300
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.knowledge.ingest import ingest_path


def main():
    parser = argparse.ArgumentParser(description="Ingest files into the knowledge base")
    parser.add_argument("source", help="File or directory to ingest")
    parser.add_argument(
        "--persist-dir",
        default="./chromadb_data",
        help="ChromaDB persistence directory (default: ./chromadb_data)",
    )
    parser.add_argument(
        "--backend",
        choices=["local", "voyage"],
        default="local",
        help="Embedding backend (default: local)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Target chunk size in tokens (default: 500)",
    )
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        print(f"Error: {source} does not exist")
        sys.exit(1)

    print(f"Ingesting: {source}")
    print(f"Backend: {args.backend}")
    print(f"ChromaDB dir: {args.persist_dir}")
    print(f"Chunk size: {args.chunk_size} tokens")
    print()

    start = time.time()
    stats = ingest_path(
        source_path=str(source),
        persist_dir=args.persist_dir,
        embedding_backend=args.backend,
        chunk_size=args.chunk_size,
    )
    elapsed = time.time() - start

    print()
    print(f"Done in {elapsed:.1f}s")
    print(f"  Files scanned: {stats['files_scanned']}")
    print(f"  Chunks extracted: {stats['chunks_extracted']}")
    print(f"  Chunks stored: {stats['chunks_stored']}")


if __name__ == "__main__":
    main()
