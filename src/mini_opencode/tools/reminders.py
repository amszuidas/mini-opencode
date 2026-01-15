from langchain.tools import ToolRuntime

from mini_opencode.tools.todo import TodoStatus


def generate_reminders(runtime: ToolRuntime) -> str:
    """
    Generate a formatted reminder string based on unfinished TODO items.

    Args:
        runtime: The ToolRuntime object containing the current agent state.

    Returns:
        A string containing formatted reminders, or an empty string if no reminders are needed.
    """
    todos = runtime.state.get("todos") or []
    unfinished_todos = [
        todo
        for todo in todos
        if todo.status not in (TodoStatus.completed, TodoStatus.cancelled)
    ]

    if not unfinished_todos:
        return ""

    reminders = [
        f"- {len(unfinished_todos)} todo{' is' if len(unfinished_todos) == 1 else 's are'} not completed. "
        "Before you present the final result to the user, **make sure** all the todos are completed.",
        "- Immediately update the TODO list using the `todo_write` tool.",
    ]

    return "\n\nIMPORTANT:\n" + "\n".join(reminders)
