"""Split large text chunks into smaller pieces for embedding."""

from backend.knowledge.types import Chunk

DEFAULT_CHUNK_SIZE = 500  # tokens (approximate via chars / 4)
DEFAULT_OVERLAP = 50
CHARS_PER_TOKEN = 4  # rough approximation


def chunk_texts(chunks: list[Chunk], chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[Chunk]:
    """Split chunks that exceed chunk_size into smaller overlapping pieces.

    Uses paragraph/sentence boundaries when possible, falls back to character splits.
    """
    max_chars = chunk_size * CHARS_PER_TOKEN
    overlap_chars = overlap * CHARS_PER_TOKEN
    result = []

    for chunk in chunks:
        if len(chunk.text) <= max_chars:
            result.append(chunk)
            continue

        pieces = _split_text(chunk.text, max_chars, overlap_chars)
        for i, piece in enumerate(pieces):
            result.append(
                Chunk(
                    text=piece,
                    metadata={**chunk.metadata, "chunk_index": i, "total_chunks": len(pieces)},
                )
            )

    return result


def _split_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    """Split text into overlapping pieces, preferring paragraph boundaries."""
    pieces = []
    start = 0

    while start < len(text):
        end = start + max_chars

        if end >= len(text):
            pieces.append(text[start:])
            break

        # Try to break at a paragraph boundary
        break_point = _find_break_point(text, start, end)
        pieces.append(text[start:break_point])
        start = break_point - overlap_chars

    return pieces


def _find_break_point(text: str, start: int, end: int) -> int:
    """Find the best break point near `end`, preferring paragraph > sentence > word boundaries."""
    # Look for double newline (paragraph break) in the last 20% of the chunk
    search_start = end - (end - start) // 5
    para_break = text.rfind("\n\n", search_start, end)
    if para_break > start:
        return para_break + 2

    # Look for single newline
    line_break = text.rfind("\n", search_start, end)
    if line_break > start:
        return line_break + 1

    # Look for sentence end
    for sep in (". ", "! ", "? "):
        sent_break = text.rfind(sep, search_start, end)
        if sent_break > start:
            return sent_break + len(sep)

    # Look for word boundary
    space = text.rfind(" ", search_start, end)
    if space > start:
        return space + 1

    return end
