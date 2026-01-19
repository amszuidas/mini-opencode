from pathlib import Path

from langchain.tools import ToolRuntime, tool

from mini_opencode.tools.reminders import generate_reminders

from .text_editor import TextEditor


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
