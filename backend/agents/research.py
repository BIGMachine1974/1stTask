"""Research Agent — web searching, doc reading, summarization."""

from pathlib import Path

from backend.mcp_servers.knowledge_server import knowledge_search

PROMPT_PATH = Path(__file__).parent / "prompts" / "research.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

# Tools available to the Research Agent
CUSTOM_TOOLS = [knowledge_search]

# Agent definition for use as a subagent
AGENT_CONFIG = {
    "name": "research",
    "description": "Research specialist — searches the web, reads docs, and provides cited summaries. Use for information gathering, fact-checking, and analysis tasks.",
    "system_prompt": SYSTEM_PROMPT,
    "custom_tools": CUSTOM_TOOLS,
}
