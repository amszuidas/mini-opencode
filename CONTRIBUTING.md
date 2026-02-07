# Contributing to mini-OpenCode

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to mini-OpenCode. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🚀 Getting Started

### Prerequisites

- **Python 3.12** or higher
- **[uv](https://github.com/astral-sh/uv)** package manager (highly recommended for dependency management)

### Installation

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/mini-opencode.git
    cd mini-opencode
    ```
3.  **Install dependencies**:
    ```bash
    uv sync
    # Or using make
    make install
    ```

## 🛠️ Development Workflow

### Running the Application

To run the mini-OpenCode CLI application:
```bash
uv run -m mini_opencode /path/to/project
# Or using python
python -m mini_opencode /path/to/project
```

### Running the Development Server

To start the LangGraph development server for visualization and debugging:
```bash
make dev
# or manually:
# uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --no-browser --allow-blocking
```

## 📏 Code Style Guidelines

We strictly follow specific coding standards to maintain codebase quality. Please ensure your contributions adhere to these guidelines.

### Python Version
- **Python 3.12+** is required.
- Use modern Python features and syntax.

### Formatting and Naming
- **File naming**: `snake_case` (e.g., `coding_agent.py`)
- **Class naming**: `PascalCase` (e.g., `ConsoleApp`, `TextEditor`)
- **Function/Variable naming**: `snake_case` (e.g., `create_coding_agent`, `plugin_tools`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `TOOL_MAP`)

### Type Hints
- **Mandatory** for all function parameters and return values.
- Use `T | None` for nullable types instead of `Optional[T]`.
- Use built-in generics `list[T]`, `dict[K, V]` instead of `List`, `Dict`.

### Documentation
- Use **Google-style docstrings** for all public modules, classes, and functions.
- Include `Args` and `Returns` sections.

### Imports Organization
Follow this order:
1. Standard library imports
2. Third-party imports
3. Local application imports (`mini_opencode`)

## 🤝 Pull Request Process

1.  **Create a Feature Branch**:
    ```bash
    git checkout -b feature/AmazingFeature
    ```
2.  **Commit your Changes**:
    Follow [Semantic Commits](https://www.conventionalcommits.org/) conventions.
    ```bash
    git commit -m 'feat: Add some AmazingFeature'
    ```
3.  **Push to the Branch**:
    ```bash
    git push origin feature/AmazingFeature
    ```
4.  **Open a Pull Request**:
    Go to the original repository and open a Pull Request describing your changes.

## 📄 License

By contributing, you agree that your contributions will be licensed under its MIT License.
