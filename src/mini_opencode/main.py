"""
Main entry point for the mini-OpenCode application.
"""

import sys
from pathlib import Path

from .cli import ConsoleApp
from .project import project


def main() -> None:
    """
    Main execution function for mini-OpenCode.

    Parses command line arguments to set the project root directory.
    """
    if len(sys.argv) > 1:
        new_root = Path(sys.argv[1])
    else:
        new_root = Path.cwd()

    try:
        project.root_dir = new_root
        print(f"Project root set to: {project.root_dir}")
        print(f"Project root set to: {project.root_dir}")
        print(f"Project root set to: {project.root_dir}")
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    app = ConsoleApp()
    app.run()
