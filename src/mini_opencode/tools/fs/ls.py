import fnmatch
from pathlib import Path
from typing import Optional

from langchain.tools import ToolRuntime, tool

from mini_opencode.tools.reminders import generate_reminders

from .ignore import DEFAULT_IGNORE_PATTERNS


@tool("ls", parse_docstring=True)
def ls_tool(
    runtime: ToolRuntime,
    path: str,
    match: Optional[list[str]] = None,
    ignore: Optional[list[str]] = None,
) -> str:
    """Lists files and directories in a given path. Optionally provide an array of glob patterns to match and ignore.

    Args:
        path: The absolute path to list files and directories from. Relative paths are **not** allowed.
        match: An optional array of glob patterns to match.
        ignore: An optional array of glob patterns to ignore.

    Returns:
        A formatted string listing the files and directories in the path, or an error message.
    """
    reminders = generate_reminders(runtime)

    _path = Path(path)
    if not _path.is_absolute():
        return f"Error: the path {path} is not an absolute path. Please provide an absolute path.{reminders}"
    if not _path.exists():
        return f"Error: the path {path} does not exist. Please provide a valid path.{reminders}"

    if not _path.is_dir():
        return f"Error: the path {path} is not a directory. Please provide a valid directory path.{reminders}"

    # Get all items in the directory
    try:
        items = list(_path.iterdir())
    except PermissionError:
        return f"Error: permission denied to access the path {path}.{reminders}"

    # Sort items: directories first, then files, both alphabetically
    items.sort(key=lambda x: (x.is_file(), x.name.lower()))

    def should_exclude(name: str, patterns: list[str]) -> bool:
        """Check if a file name matches any of the given ignore patterns."""
        for pattern in patterns:
            # Handle directory-style ignore patterns (e.g., "node_modules/**")
            clean_pattern = pattern.rstrip("/**").rstrip("/*")
            if fnmatch.fnmatch(name, clean_pattern):
                return True
        return False

    # Apply match patterns if provided
    if match:
        filtered_items = []
        for item in items:
            if any(fnmatch.fnmatch(item.name, pattern) for pattern in match):
                filtered_items.append(item)
        items = filtered_items

    # Apply ignore patterns (default + user provided)
    all_ignore = ignore or []
    if not match:
        all_ignore += DEFAULT_IGNORE_PATTERNS

    if all_ignore:
        items = [item for item in items if not should_exclude(item.name, all_ignore)]

    # Format the output
    if not items:
        return f"No items found in {path}.{reminders}"

    result_lines = []
    for item in items:
        if item.is_dir():
            result_lines.append(item.name + "/")
        else:
            result_lines.append(item.name)

    return (
        f"Here's the result in {path}: \n```\n"
        + "\n".join(result_lines)
        + f"\n```{reminders}"
    )
