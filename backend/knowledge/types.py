"""Types for the knowledge pipeline."""

from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A piece of text with metadata, ready for embedding."""

    text: str
    metadata: dict = field(default_factory=dict)
