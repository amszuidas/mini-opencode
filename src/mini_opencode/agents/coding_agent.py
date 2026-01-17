import os

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langgraph.checkpoint.base import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from mini_opencode import project
from mini_opencode.models import init_chat_model
from mini_opencode.prompts import apply_prompt_template
from mini_opencode.tools import (
    bash_tool,
    edit_tool,
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
    return create_agent(
        model=init_chat_model(),
        tools=[
            bash_tool,
            edit_tool,
            grep_tool,
            ls_tool,
            read_tool,
            todo_write_tool,
            tree_tool,
            web_crawl_tool,
            web_search_tool,
            write_tool,
            *plugin_tools,
        ],
        system_prompt=apply_prompt_template(
            "coding_agent", PROJECT_ROOT=project.root_dir
        ),
        state_schema=CodingAgentState,
        checkpointer=checkpointer,
        name="coding_agent",
        **kwargs,
    )


def create_coding_agent_for_debug(config: RunnableConfig):
    project.root_dir = os.getenv("PROJECT_ROOT", os.getcwd())
    return create_coding_agent(debug=True)
