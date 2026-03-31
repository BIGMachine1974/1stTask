"""DevOps Agent — files, APIs, databases, deployments."""

from pathlib import Path

from backend.mcp_servers.knowledge_server import knowledge_search

PROMPT_PATH = Path(__file__).parent / "prompts" / "devops.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

# Tools available to the DevOps Agent
CUSTOM_TOOLS = [knowledge_search]

# Agent definition for use as a subagent
AGENT_CONFIG = {
    "name": "devops",
    "description": "DevOps and infrastructure specialist — works with files, APIs, databases, scripts, and deployments. Use for technical operations, automation, and troubleshooting.",
    "system_prompt": SYSTEM_PROMPT,
    "custom_tools": CUSTOM_TOOLS,
}
