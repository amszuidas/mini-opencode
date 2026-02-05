from pathlib import Path

from langchain.tools import tool

from .text_editor import TextEditor


@tool("edit", parse_docstring=True)
def edit_tool(
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
    try:
        editor = TextEditor()
        editor.validate_path(_path)
        editor.edit(_path, old_str, new_str)
        return f"Successfully updated {_path}."
    except Exception as e:
        return f"Error: {e}"
