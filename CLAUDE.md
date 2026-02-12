# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the agent on a target project
uv run -m mini_opencode /path/to/project

# Build the package
uv build

# Start LangGraph dev server (for graph visualization)
make dev
# Opens at: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

# Lint/format
ruff check .
ruff format .
```

No automated test suite is currently present.

## Configuration

Copy `config.example.yaml` to `config.yaml` and `.example.env` to `.env`. The config supports:
- **models.chat_model**: LLM provider (deepseek, kimi, openai) with API key via `$ENV_VAR`
- **tools.enabled**: List of optional tools (`web_search`, `web_fetch`, `bocha_web_search`)
- **tools.mcp_servers**: Dynamic MCP tool servers (streamable_http or stdio transport)

## Architecture

### Agent Layer (`src/mini_opencode/agents/`)
`create_coding_agent()` in `coding_agent.py` builds the LangGraph agent via `deepagents.create_deep_agent()`. It wires together:
- The LLM (from `models/chat_model.py`)
- Built-in deepagents tools (file ops: `read_file`, `write_file`, `edit_file`, `glob`, `grep`; shell: `execute`; task management: `write_todos`; sub-agents: `task`)
- Optional custom tools from `tools/` (web search, date, MCP)
- Jinja2-rendered system prompt from `prompts/templates/coding_agent.md`
- `MemorySaver` checkpointer for conversation state
- Auto-discovered skills from the target project's `skills/` directory

### CLI Layer (`src/mini_opencode/cli/`)
Textual-based TUI with:
- **`app.py`** (`ConsoleApp`): Root Textual app, 3:4 left/right split layout
- **`controllers/agent_controller.py`**: Core logic — initializes agent, streams responses via `astream()`, routes tool calls to UI panels (terminal tools → `TerminalView`, file tools → `EditorView` tabs, todos → `TodoView`)
- **`controllers/command_controller.py`**: Handles slash commands (`/clear`, `/exit`)
- **Components**: `chat/`, `editor/`, `terminal/`, `todo/` under `cli/components/`

### Message Streaming Flow
`AgentController.handle_user_input()` streams two modes simultaneously:
- `"messages"`: Real-time token chunks (supports `Overwrite` for replacing prior output)
- `"updates"`: Node-level state updates for tool call routing

### Config System (`src/mini_opencode/config/config.py`)
Thread-safe singleton loaded once: `.env` → environment → `config.yaml` with `$VAR` expansion.

### Project Context (`src/mini_opencode/project.py`)
Simple singleton storing the target project root path, used by tools for file/shell operations.

## Code Conventions (from CONTRIBUTING.md)
- Python 3.12+, type hints mandatory using `T | None` syntax (not `Optional[T]`)
- Google-style docstrings
- `snake_case` functions/files, `PascalCase` classes, `UPPER_SNAKE_CASE` constants
- Import order: stdlib → third-party → local
- Ruff for formatting
