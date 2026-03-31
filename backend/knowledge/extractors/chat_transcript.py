"""Extract text from chat transcripts exported from Claude, ChatGPT, and other LLMs."""

import json
from pathlib import Path
from typing import Generator

from backend.knowledge.types import Chunk


def _extract_claude_export(data: dict, source_path: str) -> Generator[Chunk, None, None]:
    """Parse Claude conversation export format."""
    # Claude exports: {"name": "...", "chat_messages": [{"sender": "human"|"assistant", "text": "..."}]}
    title = data.get("name", "Untitled")
    messages = data.get("chat_messages", [])
    for i, msg in enumerate(messages):
        text = msg.get("text", "")
        if not text.strip():
            continue
        yield Chunk(
            text=text,
            metadata={
                "source_file": source_path,
                "source_type": "conversation",
                "conversation_title": title,
                "role": msg.get("sender", "unknown"),
                "message_index": i,
            },
        )


def _extract_chatgpt_export(data: list | dict, source_path: str) -> Generator[Chunk, None, None]:
    """Parse ChatGPT conversation export format."""
    # ChatGPT exports: [{"title": "...", "mapping": {"id": {"message": {"content": {"parts": [...]}}}}}]
    conversations = data if isinstance(data, list) else [data]
    for conv in conversations:
        title = conv.get("title", "Untitled")
        mapping = conv.get("mapping", {})
        for node_id, node in mapping.items():
            message = node.get("message")
            if not message:
                continue
            content = message.get("content", {})
            parts = content.get("parts", [])
            text = "\n".join(str(p) for p in parts if isinstance(p, str))
            if not text.strip():
                continue
            role = message.get("author", {}).get("role", "unknown")
            yield Chunk(
                text=text,
                metadata={
                    "source_file": source_path,
                    "source_type": "conversation",
                    "conversation_title": title,
                    "role": role,
                },
            )


def _extract_generic_json(data: dict | list, source_path: str) -> Generator[Chunk, None, None]:
    """Fallback: extract any JSON with messages/content arrays."""
    messages = []
    if isinstance(data, list):
        messages = data
    elif isinstance(data, dict):
        for key in ("messages", "content", "data", "conversations"):
            if key in data and isinstance(data[key], list):
                messages = data[key]
                break

    for i, item in enumerate(messages):
        if isinstance(item, str):
            text = item
        elif isinstance(item, dict):
            text = item.get("content", "") or item.get("text", "") or item.get("message", "")
        else:
            continue
        if not str(text).strip():
            continue
        yield Chunk(
            text=str(text),
            metadata={
                "source_file": source_path,
                "source_type": "conversation",
                "message_index": i,
            },
        )


def extract_chat_transcript(path: Path) -> list[Chunk]:
    """Extract chunks from a chat transcript file (JSON)."""
    with open(path) as f:
        data = json.load(f)

    source = str(path)
    chunks = []

    # Detect format
    if isinstance(data, dict) and "chat_messages" in data:
        chunks.extend(_extract_claude_export(data, source))
    elif isinstance(data, list) and data and isinstance(data[0], dict) and "mapping" in data[0]:
        chunks.extend(_extract_chatgpt_export(data, source))
    elif isinstance(data, dict) and "mapping" in data:
        chunks.extend(_extract_chatgpt_export(data, source))
    else:
        chunks.extend(_extract_generic_json(data, source))

    return chunks
