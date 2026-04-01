from dataclasses import dataclass
from pathlib import Path

from claude_code_sdk import query, ClaudeCodeOptions, AgentDefinition

from backend.config import settings
from backend.mcp_servers.knowledge_server import knowledge_search
from backend.agents.research import AGENT_CONFIG as RESEARCH_CONFIG
from backend.agents.writing import AGENT_CONFIG as WRITING_CONFIG
from backend.agents.devops import AGENT_CONFIG as DEVOPS_CONFIG

PROMPT_PATH = Path(__file__).parent / "prompts" / "manager.md"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

# Knowledge search available directly to the manager
CUSTOM_TOOLS = [knowledge_search]

# Specialist subagents
SUBAGENTS = [
    AgentDefinition(
        name=RESEARCH_CONFIG["name"],
        description=RESEARCH_CONFIG["description"],
        system_prompt=RESEARCH_CONFIG["system_prompt"],
        custom_tools=RESEARCH_CONFIG["custom_tools"],
    ),
    AgentDefinition(
        name=WRITING_CONFIG["name"],
        description=WRITING_CONFIG["description"],
        system_prompt=WRITING_CONFIG["system_prompt"],
        custom_tools=WRITING_CONFIG["custom_tools"],
    ),
    AgentDefinition(
        name=DEVOPS_CONFIG["name"],
        description=DEVOPS_CONFIG["description"],
        system_prompt=DEVOPS_CONFIG["system_prompt"],
        custom_tools=DEVOPS_CONFIG["custom_tools"],
    ),
]

AGENT_NAMES = {"research", "writing", "devops"}


@dataclass
class AgentEvent:
    """Structured event from the agent pipeline."""
    type: str  # "text", "agent_start", "agent_stop", "tool_use"
    content: str = ""
    agent_name: str = ""


async def run_agent(user_message: str, history: list[dict] | None = None):
    """Run the Managing Agent with a user message and yield AgentEvents.

    Yields:
        AgentEvent objects with type, content, and optional agent_name.
    """
    prompt_parts = []
    if history:
        prompt_parts.append("Previous conversation:\n")
        for msg in history[-20:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt_parts.append(f"{role}: {msg['content']}\n\n")
        prompt_parts.append("---\n\n")
    prompt_parts.append(f"User: {user_message}")

    full_prompt = "".join(prompt_parts)

    async for event in query(
        prompt=full_prompt,
        options=ClaudeCodeOptions(
            model=settings.AGENT_MODEL,
            system_prompt=SYSTEM_PROMPT,
            custom_tools=CUSTOM_TOOLS,
            agents=SUBAGENTS,
        ),
    ):
        # Detect subagent start/stop events
        event_type = getattr(event, "type", "")
        if event_type == "agent" and hasattr(event, "agent"):
            agent_name = getattr(event.agent, "name", "")
            status = getattr(event, "status", "")
            if status == "start":
                yield AgentEvent(type="agent_start", agent_name=agent_name)
            elif status == "stop":
                yield AgentEvent(type="agent_stop", agent_name=agent_name)
            continue

        # Text content from the agent
        if hasattr(event, "content"):
            for block in event.content:
                if hasattr(block, "text"):
                    yield AgentEvent(type="text", content=block.text)

        # Tool use events (for status display)
        if hasattr(event, "tool_name"):
            yield AgentEvent(
                type="tool_use",
                content=getattr(event, "tool_name", ""),
            )
