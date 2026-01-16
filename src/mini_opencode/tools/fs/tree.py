import fnmatch
from pathlib import Path
from typing import Optional

from langchain.tools import tool

from .ignore import DEFAULT_IGNORE_PATTERNS


def should_ignore(path: Path, root_dir: Path, ignore_patterns: list[str]) -> bool:
    """Check if a path should be ignored based on ignore patterns."""
    name = path.name
    try:
        # Get path relative to the root being searched
        rel_path = path.relative_to(root_dir)
        rel_path_str = str(rel_path)
    except ValueError:
        rel_path_str = str(path)

    for pattern in ignore_patterns:
        # Remove /** or /* suffix for matching
        if pattern.endswith("/**"):
            clean_pattern = pattern[:-3]
        elif pattern.endswith("/*"):
            clean_pattern = pattern[:-2]
        else:
            clean_pattern = pattern

        # Match against the name (e.g., "node_modules") or relative path
        if (
            fnmatch.fnmatch(name, clean_pattern)
            or fnmatch.fnmatch(rel_path_str, pattern)
            or fnmatch.fnmatch(rel_path_str, clean_pattern)
        ):
            return True

    return False


def generate_tree(
    directory: Path,
    root_dir: Path,
    prefix: str = "",
    max_depth: Optional[int] = None,
    current_depth: int = 0,
    ignore_patterns: Optional[list[str]] = None,
) -> tuple[list[str], int, int]:
    """Recursively generate tree structure and return (lines, dir_count, file_count)."""
    if ignore_patterns is None:
        ignore_patterns = []

    lines = []
    dir_count = 0
    file_count = 0

    # Check depth limit
    if max_depth is not None and current_depth >= max_depth:
        return lines, dir_count, file_count

    try:
        # Get all entries and sort them (directories first, then files)
        entries = sorted(
            directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())
        )

        # Filter out ignored entries
        entries = [
            e for e in entries if not should_ignore(e, root_dir, ignore_patterns)
        ]

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1

            # Determine the tree characters
            if is_last:
                connector = "└── "
                extension = "    "
            else:
                connector = "├── "
                extension = "│   "

            # Add the entry
            if entry.is_dir():
                lines.append(f"{prefix}{connector}{entry.name}/")
                dir_count += 1
                # Recurse into subdirectory
                if max_depth is None or current_depth + 1 < max_depth:
                    sub_lines, sub_dirs, sub_files = generate_tree(
                        entry,
                        root_dir,
                        prefix + extension,
                        max_depth,
                        current_depth + 1,
                        ignore_patterns,
                    )
                    lines.extend(sub_lines)
                    dir_count += sub_dirs
                    file_count += sub_files
            else:
                lines.append(f"{prefix}{connector}{entry.name}")
                file_count += 1

    except PermissionError:
        lines.append(f"{prefix}[Permission Denied]")

    return lines, dir_count, file_count


@tool("tree", parse_docstring=True)
def tree_tool(
    path: Optional[str] = None,
    max_depth: Optional[int] = 3,
) -> str:
    """Display directory structure in a tree format, similar to the 'tree' command.

    Shows files and directories in a hierarchical tree structure.
    Automatically excludes common ignore patterns (version control, dependencies, build artifacts, etc.).

    Args:
        path: Directory path to display. Defaults to current working directory if not specified.
        max_depth: Maximum depth to traverse. The max_depth should be less than or equal to 3. Defaults to 3.

    Returns:
        A tree-structured view of the directory as a string.
    """
    # Set search path
    search_path = Path(path).expanduser() if path else Path.cwd()

    try:
        # Validate path
        if not search_path.exists():
            return f"Error: Path '{search_path}' does not exist."

        if not search_path.is_dir():
            return f"Error: Path '{search_path}' is not a directory."

        # Enforce max_depth constraint
        if max_depth is not None and max_depth > 3:
            max_depth = 3

        # Generate tree
        resolved_path = search_path.resolve()
        lines = [str(resolved_path) + "/"]
        tree_lines, dir_count, file_count = generate_tree(
            resolved_path,
            root_dir=resolved_path,
            max_depth=max_depth,
            ignore_patterns=DEFAULT_IGNORE_PATTERNS,
        )
        lines.extend(tree_lines)

        # Add summary
        lines.append("")
        lines.append(f"{dir_count} directories, {file_count} files")

        output = "\n".join(lines)

        # Format the result
        return f"Here's the result in {search_path}:\n\n```\n{output}\n```"

    except Exception as e:
        return f"Error: {str(e)}"
