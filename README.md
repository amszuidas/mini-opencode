<div align="center">

# mini-OpenCode

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Google](https://img.shields.io/badge/code%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html)

[简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja.md)

**mini-OpenCode** is a lightweight, experimental AI Coding Agent inspired by [Deer-Code](https://github.com/MagicCube/deer-code) and [OpenCode](https://github.com/anomalyco/opencode). It demonstrates how Large Language Models (LLMs) can plan, reason, and iteratively write code with minimal infrastructure. Built on [LangGraph](https://github.com/langchain-ai/langgraph), it serves as a hackable foundation for understanding and building agentic coding systems.

<br/>
<img src="docs/images/tui_light_theme.png" width="45%" alt="Light Theme"/>
<img src="docs/images/tui_dark_theme.png" width="45%" alt="Dark Theme"/>
<br/>

</div>

---

## ✨ Features

- **🤖 DeepAgents Powered**: Built on `create_deep_agent` from the LangChain ecosystem, providing a robust foundation for agentic coding.
- **📝 Integrated Task Management**: Built-in `write_todos` tool to manage and track complex, multi-step tasks effectively.
- **🛠️ Essential Toolset**:
    - **File Operations**: Built-in tools for `ls`, `read_file`, `write_file`, `edit_file`, `glob`, and `grep`.
    - **Shell Execution**: Built-in `execute` tool for running shell commands safely.
    - **Web Capabilities**: Configurable web search and web crawling tools, with support for **MCP (Model Context Protocol)** extensions.
- **🧩 SubAgents Mechanism**: Includes a default `general-purpose` SubAgent to handle auxiliary tasks.
- **🚀 Skills System**: Automatically recognizes and utilizes user-defined Skills to enhance agent capabilities.
- **🧠 Intelligent Context Management**:
    - **AGENTS.md Injection**: Automatically detects and injects `AGENTS.md` content into the context.
    - **SummarizationMiddleware**: Automatically summarizes conversation history when context limits are reached.
    - **Large Output Handling**: Automatically evicts large tool outputs to the file system to prevent context window saturation.
    - **Robustness**: Includes `PatchToolCallsMiddleware` to handle dangling tool calls gracefully.
- **🎨 Beautiful TUI**: A polished Terminal User Interface based on Textual, featuring dark/light mode switching and streaming output.
- **⚡️ Slash Commands**: Support for slash commands (e.g., `/clear`, `/exit`) for quick actions.
- **⚙️ Highly Configurable**: Fully customizable models, tools, and behaviors via YAML configuration.

## 📖 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Acknowledgments](#-acknowledgments)
- [Star History](#-star-history)
- [License](#-license)

## 🚀 Prerequisites

- **Python 3.12** or higher
- **[uv](https://github.com/astral-sh/uv)** package manager (highly recommended for dependency management)
- API Keys for LLM (DeepSeek, Doubao) and optional web tools (Tavily, Firecrawl)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/mini-opencode.git
    cd mini-opencode
    ```

2.  **Install dependencies**
    ```bash
    uv sync
    # Or using make
    make install
    ```

## ⚙️ Configuration

1.  **Environment Variables**
    Copy the example environment file and fill in your API keys:
    ```bash
    cp .example.env .env
    ```
    Edit `.env`:
    ```ini
    DEEPSEEK_API_KEY=your_key_here
    # Optional:
    KIMI_API_KEY=your_kimi_key
    TAVILY_API_KEY=your_tavily_key
    FIRECRAWL_API_KEY=your_firecrawl_key
    ```

2.  **Application Config**
    Copy the example configuration file:
    ```bash
    cp config.example.yaml config.yaml
    ```
    Edit `config.yaml` to customize enabled tools, model parameters, and MCP servers.

3.  **LangGraph Config (Optional)**
    If you plan to use LangGraph Studio to debug the agent, copy the example LangGraph configuration file:
    ```bash
    cp langgraph.example.json langgraph.json
    ```

## 💻 Usage

### CLI Mode
Run the agent directly on a project directory:
```bash
uv run -m mini_opencode /absolute/path/to/target/project
# Or using python
python -m mini_opencode /absolute/path/to/target/project
```

### Development Mode (LangGraph Studio)
Start the LangGraph development server to visualize and interact with the agent:
```bash
make dev
```
Then open [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024) in your browser.

## 🏗️ Project Structure

```text
mini-opencode/
├── src/mini_opencode/
│   ├── agents/           # Agent creation logic (based on deepagents)
│   ├── cli/              # Terminal UI (Textual) components
│   ├── config/           # Configuration loading & validation
│   ├── models/           # LLM model factory & setup
│   ├── prompts/          # Prompt templates (Jinja2)
│   ├── tools/            # Additional tool implementations
│   │   ├── date/         # Date tool
│   │   ├── mcp/          # MCP tools integration
│   │   └── web/          # Web Search & Crawl
│   ├── main.py           # CLI entry point
│   └── project.py        # Project context manager
├── skills/               # Agent Skills (instructions, scripts, and references)
├── config.example.yaml   # Template configuration
├── langgraph.example.json# Template LangGraph config
├── Makefile              # Build & run commands
└── pyproject.toml        # Project dependencies & metadata
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (follow [Semantic Commits](https://www.conventionalcommits.org/), e.g., `git commit -m 'feat: Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## 🙏 Acknowledgments

Special thanks to the developers of the following projects for their inspiration and architectural references:

- **[Deer-Code](https://github.com/MagicCube/deer-code)**
- **[OpenCode](https://github.com/anomalyco/opencode)**

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=amszuidas/mini-opencode&type=Date)](https://star-history.com/#amszuidas/mini-opencode&Date)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ using [LangGraph](https://langchain-ai.github.io/langgraph/) and [Textual](https://textual.textualize.io/).*
