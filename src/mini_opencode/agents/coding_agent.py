import os
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langchain.tools import BaseTool
from langgraph.checkpoint.base import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from mini_opencode import project
from mini_opencode.config import get_config_section
from mini_opencode.models import init_chat_model
from mini_opencode.prompts import apply_prompt_template
from mini_opencode.tools import (
    get_current_date_tool,
    web_fetch_tool,
    web_search_tool,
)

TOOL_MAP = {
    "get_current_date": get_current_date_tool,
    "web_fetch": web_fetch_tool,
    "web_search": web_search_tool,
}


def create_coding_agent(
    plugin_tools: list[BaseTool] = [], checkpointer: MemorySaver | None = None, **kwargs
):
    """Create a coding agent.

    Args:
        plugin_tools: Additional tools to add to the agent.
        checkpointer: Checkpointer to use for the agent.
        **kwargs: Additional keyword arguments to pass to the agent.

    Returns:
        The coding agent.
    """
    # Initialize model
    model = init_chat_model()

    # Initialize tools
    # create_deep_agent default supported tools:
    # - `write_todos`: manage a todo list
    # - `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`: file operations
    # - `execute`: run shell commands
    # - `task`: call subagents
    # The `execute` tool allows running shell commands if the backend implements SandboxBackendProtocol. For non-sandbox backends, the execute tool will return an error message.
    enabled_tools_config = get_config_section(["tools", "enabled"])
    if enabled_tools_config is not None and isinstance(enabled_tools_config, list):
        tools = [TOOL_MAP[name] for name in enabled_tools_config if name in TOOL_MAP]
        # Add get_current_date_tool if not enabled
        if "get_current_date" not in enabled_tools_config:
            tools.append(get_current_date_tool)
    else:
        tools = [
            get_current_date_tool,
            web_fetch_tool,
            web_search_tool,
        ]
    tools = [*tools, *plugin_tools]

    # Initialize system prompt
    system_prompt = apply_prompt_template(
        "coding_agent",
        PROJECT_ROOT=project.root_dir,
    )

    # Initialize middleware
    # create_deep_agent default supported middleware:
    # - `TodoListMiddleware`: todo list management
    # - `FilesystemMiddleware`: providing file system and optional `execution` tools
    # - `SubAgentMiddleware`: providing subagents via a `task` tool
    # - `SummarizationMiddleware`: providing context summarization
    # - `AnthropicPromptCachingMiddleware`: caching Anthropic prompts
    # - `PatchToolCallsMiddleware`: patching dangling tool calls in the messages history

    # Initialize subagents
    # create_deep_agent default supported subagents:
    # - `general-purpose`: General-purpose agent for researching complex questions, searching for files and content, and executing multi-step tasks.

    # Initialize skills
    skills = []
    skills_dir = Path(project.root_dir) / "skills"
    if skills_dir.exists():
        skills.append(str(skills_dir.absolute()))

    # Initialize memory
    memory = []
    agents_md_path = Path(project.root_dir) / "AGENTS.md"
    if agents_md_path.exists():
        memory.append(str(agents_md_path.absolute()))

    # Initialize backend
    backend = FilesystemBackend(root_dir=project.root_dir)

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        skills=skills,
        memory=memory,
        backend=backend,
        checkpointer=checkpointer,
        name="coding_agent",
        **kwargs,
    )


def create_coding_agent_for_debug(config: RunnableConfig):
    project.root_dir = os.getenv("PROJECT_ROOT", os.getcwd())
    return create_coding_agent(debug=True)
