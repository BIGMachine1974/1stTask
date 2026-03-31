"""Extract text from code repositories."""

from pathlib import Path
from typing import Generator

from backend.knowledge.types import Chunk

# Extensions we want to index
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
    ".sh", ".bash", ".zsh", ".sql", ".yaml", ".yml", ".toml", ".json",
    ".md", ".txt", ".cfg", ".ini", ".env.example",
}

# Files to skip
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "dist",
    "build", ".next", ".nuxt", "target", ".tox", ".mypy_cache",
}

MAX_FILE_SIZE = 100_000  # 100KB


def extract_code_repo(path: Path) -> list[Chunk]:
    """Extract chunks from a code repository directory.

    Each file becomes one chunk (large files get split by the chunker later).
    README and config files get tagged with higher relevance.
    """
    chunks = []

    if path.is_file():
        chunk = _extract_single_file(path)
        if chunk:
            chunks.append(chunk)
        return chunks

    for file_path in _walk_code_files(path):
        chunk = _extract_single_file(file_path)
        if chunk:
            chunks.append(chunk)

    return chunks


def _walk_code_files(root: Path) -> Generator[Path, None, None]:
    """Walk a directory tree yielding code files."""
    for item in root.rglob("*"):
        if any(skip in item.parts for skip in SKIP_DIRS):
            continue
        if item.is_file() and item.suffix in CODE_EXTENSIONS:
            if item.stat().st_size <= MAX_FILE_SIZE:
                yield item


def _extract_single_file(path: Path) -> Chunk | None:
    """Extract a chunk from a single code file."""
    try:
        text = path.read_text(errors="replace")
    except (OSError, UnicodeDecodeError):
        return None

    if not text.strip():
        return None

    # Determine if this is a high-value file
    name_lower = path.name.lower()
    is_readme = name_lower.startswith("readme")
    is_config = name_lower in {
        "package.json", "pyproject.toml", "cargo.toml", "go.mod",
        "dockerfile", "docker-compose.yml", "makefile",
    }

    return Chunk(
        text=text,
        metadata={
            "source_file": str(path),
            "source_type": "code",
            "language": path.suffix.lstrip("."),
            "filename": path.name,
            "is_readme": is_readme,
            "is_config": is_config,
        },
    )
