from pathlib import Path

from langchain.tools import tool

from .text_editor import TextEditor


@tool("read", parse_docstring=True)
def read_tool(
    path: str,
    read_range: list[int] | None = None,
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
    try:
        editor = TextEditor()
        editor.validate_path(_path)
        content = editor.read(_path, read_range)
        return f"Here's the result of reading {_path}:\n\n```\n{content}\n```"
    except Exception as e:
        return f"Error: {e}"
