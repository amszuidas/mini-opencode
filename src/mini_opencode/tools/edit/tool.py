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


@tool("write", parse_docstring=True)
def write_tool(
    runtime: ToolRuntime,
    path: str,
    content: str = "",
) -> str:
    """
    Write content to a file. Can be used to create or overwrite a file.

    Args:
        path: The absolute path to the file. Only absolute paths are supported.
        content: The text to write to the file.
    """
    _path = Path(path)
    reminders = generate_reminders(runtime)
    try:
        editor = TextEditor()
        editor.validate_path(_path)
        if _path.is_dir():
            return f"Error: The path {_path} is a directory. Please provide a valid file path.{reminders}"
        editor.write_file(_path, content)
        return f"File successfully written at {_path}.{reminders}"
    except Exception as e:
        return f"Error: {e}{reminders}"


@tool("edit", parse_docstring=True)
def edit_tool(
    runtime: ToolRuntime,
    path: str,
    old_str: str,
    new_str: str,
) -> str:
    """
    Replace a specific block of text in a file with new content.

    The `old_str` MUST be unique in the file to avoid ambiguous replacements.
    If it is not unique, the edit will fail.

    Args:
        path: The absolute path to the file. Only absolute paths are supported.
        old_str: The exact text block to replace. Must include enough context to be unique.
        new_str: The new text to insert in place of the old text.
    """
    _path = Path(path)
    reminders = generate_reminders(runtime)
    try:
        editor = TextEditor()
        editor.validate_path(_path)
        editor.edit(_path, old_str, new_str)
        return f"Successfully updated {_path}.{reminders}"
    except Exception as e:
        return f"Error: {e}{reminders}"
