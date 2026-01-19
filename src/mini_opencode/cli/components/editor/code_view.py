from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static

from mini_opencode.cli.theme import DARK_THEME, LIGHT_THEME


class CodeView(ScrollableContainer):
    """Code view component with syntax highlighting"""

    DEFAULT_CSS = """
    CodeView {
        height: 1fr;
    }

    CodeView #code-content {
        padding: 1 1;
        width: auto;
        height: auto;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = "# Welcome to mini-OpenCode\n# Code will be displayed here\n\ndef hello_world():\n    print('Hello, World!')"
        self.file_path = None

    def compose(self) -> ComposeResult:
        yield Static(id="code-content")

    def update_code(self, code: str, file_path: str = None) -> None:
        """Update code content and optionally the file path"""
        self.code = code
        self.file_path = file_path

        # Auto-detect language from file path or default to python
        if file_path:
            lexer = Syntax.guess_lexer(file_path, code)
        else:
            lexer = "text"

        # Create syntax highlighted content
        app_theme = self.app.theme
        syntax_theme = "monokai" if app_theme == "dark" else "friendly"
        bg_color = DARK_THEME.boost if app_theme == "dark" else LIGHT_THEME.boost

        syntax = Syntax(
            code,
            lexer,
            theme=syntax_theme,
            line_numbers=True,
            word_wrap=False,
            indent_guides=False,
            background_color=bg_color,
        )

        content_widget = self.query_one("#code-content", Static)
        content_widget.update(syntax)
