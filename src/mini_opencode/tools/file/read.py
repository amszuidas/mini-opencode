from pathlib import Path
from typing import Optional

from langchain.tools import ToolRuntime, tool

from mini_opencode.tools.reminders import generate_reminders

from .text_editor import TextEditor


@tool("read", parse_docstring=True)
def read_tool(
    runtime: ToolRuntime,
    path: str,
    read_range: Optional[list[int]] = None,
) -> str:
    """
    Read the content of a file with line numbers.

    Args:
        path: The absolute path to the file. Only absolute paths are supported.
        read_range:
            An array of two integers [start, end] specifying the line numbers to read.
            Line numbers are 1-indexed. Use -1 for the end line to read to the end of the file.
    """
    _path = Path(path)
    reminders = generate_reminders(runtime)
    try:
        editor = TextEditor()
        editor.validate_path(_path)
        content = editor.read(_path, read_range)
        return (
            f"Here's the result of reading {_path}:\n\n```\n{content}\n```{reminders}"
        )
    except Exception as e:
        return f"Error: {e}{reminders}"
