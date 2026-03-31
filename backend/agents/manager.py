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


async def run_agent(user_message: str, history: list[dict] | None = None):
    """Run the Managing Agent with a user message and yield text chunks.

    Args:
        user_message: The new message from the user.
        history: Prior conversation messages as [{"role": "user"|"assistant", "content": "..."}].

    Yields:
        Text chunks from the agent's response.
    """
    # Build the prompt with conversation history for context
    prompt_parts = []
    if history:
        prompt_parts.append("Previous conversation:\n")
        for msg in history[-20:]:  # Last 20 messages for context window management
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
        if hasattr(event, "content"):
            # event.content is a list of content blocks
            for block in event.content:
                if hasattr(block, "text"):
                    yield block.text
