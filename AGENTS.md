# AGENTS.md - mini-OpenCode Development Guide

This document provides essential information for AI agents working in the mini-opencode codebase.

## Build, Lint, and Test Commands

### Installation and Setup
```bash
# Install dependencies using uv (Python package manager)
uv sync

# Build the package
uv build

# Run development server
make dev  # or: uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --no-browser --allow-blocking
```

### Running the Application
```bash
# Run the mini-OpenCode CLI application
python -m mini_opencode /path/to/project
```

### Testing
Currently no test framework is configured. The project uses:
- Python 3.12+ (as specified in pyproject.toml)
- No test files found in the repository
- No test commands defined in Makefile

## Code Style Guidelines

### Python Version
- **Python 3.12+** required (specified in pyproject.toml)
- Use type hints throughout the codebase

### Imports Organization
Follow this import order pattern:
1. Standard library imports
2. Third-party imports (langchain, textual, etc.)
3. Local application imports (mini_opencode modules)

Example from `src/mini_opencode/agents/coding_agent.py`:
```python
import os

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langgraph.checkpoint.base import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from mini_opencode import project
from mini_opencode.config import get_config_section
from mini_opencode.models import init_chat_model
from mini_opencode.prompts import apply_prompt_template
```

### Formatting and Naming Conventions
- **File naming**: Use snake_case for Python files (e.g., `coding_agent.py`)
- **Class naming**: Use PascalCase (e.g., `ConsoleApp`, `TextEditor`)
- **Function naming**: Use snake_case (e.g., `create_coding_agent`, `validate_path`)
- **Variable naming**: Use snake_case (e.g., `plugin_tools`, `checkpointer`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `TOOL_MAP`, `DARK_THEME`)

### Type Hints
- Always use type hints for function parameters and return values
- Use `T | None` for nullable types instead of `Optional[T]`
- Use `list[T]` and `dict[K, V]` instead of `List[T]` and `Dict[K, V]`

Example from `src/mini_opencode/tools/fs/text_editor.py`:
```python
from typing import Literal

TextEditorCommand = Literal[
    "read",
    "write",
    "edit",
]

class TextEditor:
    def validate_path(self, path: Path) -> None:
        """Check that the path is absolute."""
```

### Error Handling
- Use try-except blocks with specific exception types
- Provide helpful error messages with suggestions
- Use `raise ValueError` for invalid arguments
- Use `raise FileNotFoundError` for missing files

Example from `src/mini_opencode/main.py`:
```python
try:
    project.root_dir = new_root
    print(f"Project root set to: {project.root_dir}")
except (FileNotFoundError, NotADirectoryError) as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Documentation
- Use docstrings for all public functions, classes, and modules
- Follow Google-style docstring format with Args and Returns sections
- Include examples when helpful

Example from `src/mini_opencode/tools/fs/write.py`:
```python
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
```

### Path Handling
- Always use `pathlib.Path` for file paths
- Validate paths are absolute before using them
- Provide helpful suggestions when relative paths are provided

Example from `src/mini_opencode/tools/fs/text_editor.py`:
```python
def validate_path(self, path: Path):
    if not path.is_absolute():
        suggested_path = Path.cwd().resolve() / path
        raise ValueError(
            f"The path {path} is not an absolute path, it should start with `/`. Do you mean {suggested_path}?"
        )
```

### Tool Development Guidelines
- All tools should use the `@tool` decorator with `parse_docstring=True`
- Include comprehensive docstrings with clear parameter descriptions
- Return meaningful error messages with suggestions
- Use the `generate_reminders` function from `mini_opencode.tools.reminders`

### Project Structure Conventions
- Keep related functionality in modules under appropriate directories:
  - `agents/` - Agent implementations and state management
  - `tools/` - Tool implementations (file operations, terminal, web, etc.)
  - `cli/` - CLI and TUI components
  - `models/` - LLM model configurations
  - `prompts/` - Prompt templates
  - `config/` - Configuration management

### Configuration Management
- Use `config.yaml` for application configuration
- Access configuration via `mini_opencode.config.get_config_section()`
- Support environment variables for API keys and sensitive data

### Textual UI Development
- Follow Textual framework conventions for UI components
- Use CSS for styling with theme variables (`$background`, `$primary`, etc.)
- Implement responsive layouts with containers

## Project Rules (.trae/rules/project_rules.md)

The project includes these key guidelines:
- mini-opencode is a lightweight experimental AI Coding Agent
- Built with LangGraph for stateful, multi-step reasoning
- Supports comprehensive tool use (file operations, terminal, web search, etc.)
- Maintains conversation history and todo list in state
- Configurable through `config.yaml`
- Supports MCP (Model Context Protocol) server integration

## Environment Variables
- `DEEPSEEK_API_KEY` - DeepSeek API key
- `ARK_API_KEY` - Doubao/ARK API key  
- `FIRECRAWL_API_KEY` - Firecrawl API key for web crawling
- `TAVILY_API_KEY` - Tavily API key for web search
- `PROJECT_ROOT` - Project root directory (default: current directory)
- `MINI_OPENCODE_CONFIG` - Path to config file (default: `config.yaml`)

## Key Principles
1. **Minimal Infrastructure**: Keep the codebase simple and hackable
2. **Tool Use**: Implement comprehensive, well-documented tools
3. **State Management**: Maintain conversation context and task lists
4. **Configurability**: Make components easy to customize
5. **Error Handling**: Provide helpful error messages with suggestions
6. **Type Safety**: Use type hints throughout the codebase