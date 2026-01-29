from typing import Annotated

from langchain.messages import ToolMessage
from langchain.tools import InjectedToolCallId, tool
from langgraph.graph.state import Command

from .types import TodoItem, TodoStatus


@tool("todo_write", parse_docstring=True)
def todo_write_tool(
    todos: list[TodoItem], tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Update the entire TODO list with the latest items.

    Args:
        todos: A list of TodoItem objects representing the current state of tasks.
        tool_call_id: The unique identifier for the tool call (injected).
    """
    unfinished_todos = [
        todo
        for todo in todos
        if todo.status not in (TodoStatus.completed, TodoStatus.cancelled)
    ]

    status_msg = (
        f"{len(unfinished_todos)} todo{' is' if len(unfinished_todos) == 1 else 's are'} not completed."
        if unfinished_todos
        else "All todos are completed."
    )
    message = (
        f"Successfully updated the TODO list with {len(todos)} items. {status_msg}"
    )

    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(
                    message,
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
