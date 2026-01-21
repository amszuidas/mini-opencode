# mini-OpenCode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

mini-OpenCode is a lightweight experimental AI Coding Agent inspired by OpenCode. It explores how LLMs can plan, reason, and iteratively write code with minimal infrastructure, aiming to provide a simple, hackable foundation for understanding and building agentic coding systems.

## ✨ Features

- **🤖 Intelligent Coding Agent**: Powered by LangGraph for stateful, multi-step reasoning
- **🛠️ Comprehensive Toolset**: File operations, terminal commands, web search, web crawling, and more
- **📝 TODO Management**: Built-in todo list for tracking complex multi-step tasks
- **⚙️ Configurable**: Easy customization through YAML configuration
- **🔌 Extensible**: Support for MCP (Model Context Protocol) server integration
- **🎨 Textual UI**: Clean terminal-based interface for interaction
- **🔒 Type Safety**: Full type hints throughout the codebase

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mini-opencode
```

2. Install dependencies:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .example.env .env
# Edit .env with your API keys
```

### Configuration

1. Copy the example configuration:
```bash
cp config.example.yaml config.yaml
```

2. Edit `config.yaml` to configure:
   - LLM models (DeepSeek, etc.)
   - Enabled tools
   - API keys for web services
   - MCP server connections

### Running the Agent

#### Option 1: Direct CLI
```bash
# Run on a specific project directory
python -m mini_opencode /path/to/your/project
```

#### Option 2: Development Mode with LangGraph Studio
```bash
make dev
# Then open http://localhost:2024 in your browser
```

## 📋 Available Tools

mini-OpenCode comes with a comprehensive set of tools:

### File Operations
- **`read`**: Read file contents with line numbers
- **`write`**: Write content to files (create or overwrite)
- **`edit`**: Replace specific text blocks in files
- **`ls`**: List files and directories
- **`tree`**: Display directory structure
- **`grep`**: Search file contents with regex patterns

### System Operations
- **`bash`**: Execute bash commands in a keep-alive shell

### Web Operations
- **`web_search`**: Search the web with Tavily API
- **`web_crawl`**: Crawl websites with Firecrawl API
- **`SearchDocsByLangChain`**: Search LangChain documentation

### Task Management
- **`todo_write`**: Manage todo lists for complex multi-step tasks

## 🏗️ Project Structure

```
mini-opencode/
├── src/mini_opencode/
│   ├── agents/           # Agent implementations and state management
│   ├── tools/           # Tool implementations
│   │   ├── file/        # File operations
│   │   ├── fs/          # Filesystem operations
│   │   ├── terminal/    # Terminal commands
│   │   ├── web/         # Web operations
│   │   └── todo/        # Todo management
│   ├── cli/             # CLI and TUI components
│   ├── config/          # Configuration management
│   ├── models/          # LLM model configurations
│   ├── prompts/         # Prompt templates
│   └── project.py       # Project state management
├── config.yaml          # Main configuration file
├── langgraph.json       # LangGraph configuration
├── pyproject.toml       # Python project configuration
└── Makefile            # Build and development commands
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# LLM API Keys
DEEPSEEK_API_KEY=your_deepseek_api_key
ARK_API_KEY=your_doubao_ark_api_key

# Web Service API Keys
FIRECRAWL_API_KEY=your_firecrawl_api_key
TAVILY_API_KEY=your_tavily_api_key

# Project Configuration
PROJECT_ROOT=/path/to/your/project
MINI_OPENCODE_CONFIG=config.yaml
```

### Model Configuration

Edit `config.yaml` to configure your preferred LLM:

```yaml
models:
  chat_model:
    type: deepseek
    model: 'deepseek-chat'
    api_base: 'https://api.deepseek.com'
    api_key: $DEEPSEEK_API_KEY
    temperature: 0
    top_p: 1.0
    max_tokens: 8192
```

### Tool Configuration

Enable or disable specific tools in `config.yaml`:

```yaml
tools:
  enabled:
    - edit
    - read
    - write
    - grep
    - ls
    - tree
    - bash
    - web_crawl
    - web_search
```

## 🧠 How It Works

mini-OpenCode uses a stateful agent architecture built on LangGraph:

1. **State Management**: Maintains conversation history and todo lists
2. **Tool Selection**: Dynamically chooses appropriate tools based on user requests
3. **Multi-step Reasoning**: Breaks down complex tasks into manageable steps
4. **Error Recovery**: Provides helpful error messages and suggestions

### Agent State

The agent maintains state including:
- Conversation messages
- Todo items for task tracking
- Tool execution history

### Prompt Engineering

The agent uses carefully crafted prompts that include:
- Tool usage guidelines
- TODO management rules
- Frontend technology defaults
- Safety guidelines

## 🔧 Development

### Building from Source

```bash
# Install dependencies
uv sync

# Build the package
uv build

# Run tests (when available)
# Currently no test framework is configured
```

### Code Style

The project follows strict coding standards:

- **Python 3.12+** with full type hints
- **Google-style docstrings** for all public functions
- **Snake_case** for files, functions, and variables
- **PascalCase** for classes
- **UPPER_SNAKE_CASE** for constants

### Adding New Tools

1. Create a new tool in the appropriate directory under `src/mini_opencode/tools/`
2. Use the `@tool` decorator with `parse_docstring=True`
3. Add comprehensive docstrings with clear parameter descriptions
4. Register the tool in `src/mini_opencode/agents/coding_agent.py`

Example tool structure:
```python
@tool("your_tool_name", parse_docstring=True)
def your_tool_function(
    runtime: ToolRuntime,
    param1: str,
    param2: int = 0,
) -> str:
    """
    Brief description of what the tool does.

    Args:
        param1: Description of param1.
        param2: Description of param2 with default value.

    Returns:
        Description of what the tool returns.
    """
    # Implementation here
```

## 📚 Documentation

- **AGENTS.md**: Detailed development guide for AI agents
- **docs/**: Additional documentation
- **Prompt Templates**: Located in `src/mini_opencode/prompts/templates/`

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure code follows the project's style guidelines
5. Submit a pull request

### Development Guidelines

- Always use type hints for function parameters and return values
- Include comprehensive docstrings for all public functions
- Use `pathlib.Path` for file path operations
- Provide helpful error messages with suggestions
- Follow the import order: standard library → third-party → local imports

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [OpenCode](https://github.com/opencodeai/opencode)
- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [LangChain](https://github.com/langchain-ai/langchain) for LLM integration
- Features [Textual](https://github.com/Textualize/textual) for terminal UI

## 🔗 Related Projects

- [OpenCode](https://github.com/opencodeai/opencode) - The original inspiration
- [LangGraph](https://github.com/langchain-ai/langgraph) - Stateful agent framework
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol

## 📞 Support

For issues, questions, or feature requests:
1. Check the [AGENTS.md](AGENTS.md) documentation
2. Search existing issues
3. Open a new issue with detailed information

---

**mini-OpenCode** - A lightweight, hackable foundation for exploring AI-powered coding agents.