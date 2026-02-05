import subprocess
from typing import Literal

from langchain.tools import tool

from .ignore import DEFAULT_IGNORE_PATTERNS


@tool("grep", parse_docstring=True)
def grep_tool(
    pattern: str,
    path: str | None = None,
    glob: str | None = None,
    output_mode: Literal[
        "content", "files_with_matches", "count"
    ] = "files_with_matches",
    B: int | None = None,
    A: int | None = None,
    C: int | None = None,
    n: bool | None = None,
    i: bool | None = None,
    type: str | None = None,
    head_limit: int = 100,
    offset: int = 0,
    multiline: bool = False,
) -> str:
    """A powerful search tool built on ripgrep for searching file contents with regex patterns.

    ALWAYS use this tool for search tasks. NEVER invoke `grep` or `rg` as a Bash command.
    Supports full regex syntax, file filtering, and various output modes.

    Args:
        pattern: The regular expression pattern to search for in file contents.
                Uses ripgrep syntax - literal braces need escaping (e.g., `interface\\{\\}` for `interface{}`).
        path: File or directory to search in. Defaults to current working directory if not specified.
        glob: Glob pattern to filter files (e.g., "*.js", "*.{ts,tsx}").
        output_mode: Output mode - "content" shows matching lines with optional context,
                    "files_with_matches" shows only file paths (default),
                    "count" shows match counts per file.
        B: Number of lines to show before each match. Only works with output_mode="content".
        A: Number of lines to show after each match. Only works with output_mode="content".
        C: Number of lines to show before and after each match. Only works with output_mode="content".
        n: Show line numbers in output. Only works with output_mode="content".
        i: Enable case insensitive search.
        type: File type to search (e.g., "js", "py", "rust", "go", "java").
             More efficient than glob for standard file types.
        head_limit: Limit output to first N lines/entries. Works across all output modes. Defaults to 100.
        offset: Skip first N lines/entries before applying head_limit. Defaults to 0.
        multiline: Enable multiline mode where patterns can span lines and . matches newlines.
                  Default is False (single-line matching only).

    Returns:
        Search results as a string, formatted according to the output_mode.
    """
    # Build ripgrep command
    cmd = ["rg"]

    # Add output mode flags
    if output_mode == "files_with_matches":
        cmd.append("-l")
    elif output_mode == "count":
        cmd.append("-c")

    # Add context flags (only for content mode)
    if output_mode == "content":
        if C is not None:
            cmd.extend(["-C", str(C)])
        else:
            if B is not None:
                cmd.extend(["-B", str(B)])
            if A is not None:
                cmd.extend(["-A", str(A)])
        if n:
            cmd.append("-n")

    # Add case insensitive flag
    if i:
        cmd.append("-i")

    # Add file type filter
    if type:
        cmd.extend(["--type", type])

    # Add glob pattern
    if glob:
        cmd.extend(["--glob", glob])

    # Apply default ignore patterns
    for ignore_pattern in DEFAULT_IGNORE_PATTERNS:
        cmd.extend(["--glob", f"!{ignore_pattern}"])

    # Add multiline mode
    if multiline:
        cmd.extend(["-U", "--multiline-dotall"])

    # Add pattern
    cmd.append(pattern)

    # Add path if specified
    search_path = path if path else "."
    cmd.append(search_path)

    # Execute ripgrep
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # Don't raise on non-zero exit (no matches found)
        )

        # Check for errors (exit code 2 indicates error, 1 means no matches)
        if result.returncode == 2:
            return f"Error executing ripgrep: {result.stderr.strip()}"

        output = result.stdout

        # Apply offset and head limit if output exists
        if output:
            lines = output.splitlines()
            start = offset if offset else 0
            end = start + head_limit if head_limit else len(lines)
            output = "\n".join(lines[start:end])

        # Format the result
        if output:
            return f"Here's the result in {search_path}:\n\n```\n{output}\n```"
        elif result.returncode == 1:
            return f"No matches found in {search_path}."
        else:
            return "Search completed but no output was returned."

    except Exception as e:
        return f"Unexpected error: {str(e)}"
