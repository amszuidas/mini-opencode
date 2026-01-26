import os
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langgraph.checkpoint.base import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from mini_opencode import project
from mini_opencode.config import get_config_section
from mini_opencode.models import init_chat_model
from mini_opencode.prompts import apply_prompt_template
from mini_opencode.skills.loader import load_skills
from mini_opencode.tools import (
    bash_tool,
    edit_tool,
    get_today_date_tool,
    grep_tool,
    ls_tool,
    read_tool,
    todo_write_tool,
    tree_tool,
    web_crawl_tool,
    web_search_tool,
    write_tool,
)

from .state import CodingAgentState

TOOL_MAP = {
    "bash": bash_tool,
    "edit": edit_tool,
    "get_today_date": get_today_date_tool,
    "grep": grep_tool,
    "ls": ls_tool,
    "read": read_tool,
    "todo_write": todo_write_tool,
    "tree": tree_tool,
    "web_crawl": web_crawl_tool,
    "web_search": web_search_tool,
    "write": write_tool,
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
    enabled_tools_config = get_config_section(["tools", "enabled"])
    if enabled_tools_config is not None and isinstance(enabled_tools_config, list):
        tools = [TOOL_MAP[name] for name in enabled_tools_config if name in TOOL_MAP]
        # Add todo_write_tool and get_today_date_tool if not enabled
        if "todo_write" not in enabled_tools_config:
            tools.append(todo_write_tool)
        if "get_today_date" not in enabled_tools_config:
            tools.append(get_today_date_tool)
    else:
        tools = [
            bash_tool,
            edit_tool,
            grep_tool,
            ls_tool,
            read_tool,
            get_today_date_tool,
            todo_write_tool,
            tree_tool,
            web_crawl_tool,
            web_search_tool,
            write_tool,
        ]

    # Initialize system prompt
    package_root = Path(__file__).parent.parent.parent.parent
    skills_dir = package_root / "skills"
    skills = load_skills(skills_dir)
    skills_list_str = "\n".join(
        [f"- {skill.name}: {skill.path}\n  {skill.description}" for skill in skills]
    )

    system_prompt = apply_prompt_template(
        "coding_agent",
        PROJECT_ROOT=project.root_dir,
        SKILLS_PATH=str(skills_dir.absolute()),
        SKILLS_LIST=skills_list_str,
    )

    return create_agent(
        model=model,
        tools=[
            *tools,
            *plugin_tools,
        ],
        system_prompt=system_prompt,
        state_schema=CodingAgentState,
        checkpointer=checkpointer,
        name="coding_agent",
        **kwargs,
    )


def create_coding_agent_for_debug(config: RunnableConfig):
    project.root_dir = os.getenv("PROJECT_ROOT", os.getcwd())
    return create_coding_agent(debug=True)
