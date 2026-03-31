"""Extract text from documents: markdown, plain text, PDF."""

from pathlib import Path

from backend.knowledge.types import Chunk


def extract_document(path: Path) -> list[Chunk]:
    """Extract chunks from a document file (.md, .txt, .pdf)."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf(path)
    elif suffix in {".md", ".txt", ".rst", ".org"}:
        return _extract_text(path)
    else:
        return _extract_text(path)


def _extract_text(path: Path) -> list[Chunk]:
    """Extract from plain text / markdown files."""
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []

    if not text.strip():
        return []

    return [
        Chunk(
            text=text,
            metadata={
                "source_file": str(path),
                "source_type": "document",
                "format": path.suffix.lstrip("."),
                "filename": path.name,
            },
        )
    ]


def _extract_pdf(path: Path) -> list[Chunk]:
    """Extract text from PDF files using pymupdf if available."""
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # older pymupdf package name
        except ImportError:
            print(f"  Skipping PDF {path.name} (install pymupdf: pip install pymupdf)")
            return []

    chunks = []
    try:
        doc = pymupdf.open(str(path))
        full_text = []
        for page in doc:
            full_text.append(page.get_text())
        doc.close()

        text = "\n\n".join(full_text)
        if text.strip():
            chunks.append(
                Chunk(
                    text=text,
                    metadata={
                        "source_file": str(path),
                        "source_type": "document",
                        "format": "pdf",
                        "filename": path.name,
                        "page_count": len(full_text),
                    },
                )
            )
    except Exception as e:
        print(f"  Error reading PDF {path.name}: {e}")

    return chunks
