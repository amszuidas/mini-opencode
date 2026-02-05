import threading

from langchain.tools import tool

from mini_opencode.project import project

from .bash_terminal import BashTerminal

# Use a thread lock and global variable for the terminal instance
# In a multi-user environment, this should ideally be stored in a session-specific context
terminal_lock = threading.Lock()
keep_alive_terminal: BashTerminal | None = None


@tool("bash", parse_docstring=True)
def bash_tool(
    command: str,
    reset_cwd: bool | None = False,
    timeout: int | None = 60,
):
    """Execute a standard bash command in a keep-alive shell, and return the output if successful or error message if failed.

    Use this tool to perform:
    - Create directories
    - Install dependencies
    - Start development server
    - Run tests and linting
    - Git operations

    Never use this tool to perform any harmful or dangerous operations.

    Args:
        command: The command to execute.
        reset_cwd: Whether to reset the current working directory to the project root directory.
        timeout: Maximum time to wait for the command to complete (in seconds). Default is 60.
    """
    global keep_alive_terminal

    with terminal_lock:
        try:
            if keep_alive_terminal is None:
                keep_alive_terminal = BashTerminal(project.root_dir)
            elif reset_cwd:
                keep_alive_terminal.close()
                keep_alive_terminal = BashTerminal(project.root_dir)

            output = keep_alive_terminal.execute(command, timeout=timeout)
        except Exception as e:
            output = f"Error executing command: {str(e)}"
            # If terminal crashed, clear it so it can be recreated next time
            if keep_alive_terminal:
                try:
                    keep_alive_terminal.close()
                except Exception:
                    pass
            keep_alive_terminal = None

    return f"```\n{output}\n```"
