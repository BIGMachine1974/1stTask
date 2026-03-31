"""Writing Agent — drafting, editing, formatting documents."""

from pathlib import Path

from backend.mcp_servers.knowledge_server import knowledge_search

PROMPT_PATH = Path(__file__).parent / "prompts" / "writing.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

# Tools available to the Writing Agent
CUSTOM_TOOLS = [knowledge_search]

# Agent definition for use as a subagent
AGENT_CONFIG = {
    "name": "writing",
    "description": "Writing and documentation specialist — drafts, edits, and formats content. Use for documents, emails, proposals, README files, and any text content.",
    "system_prompt": SYSTEM_PROMPT,
    "custom_tools": CUSTOM_TOOLS,
}
