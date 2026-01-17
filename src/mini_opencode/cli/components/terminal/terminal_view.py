from textual.containers import VerticalScroll
from textual.widgets import Static


class TerminalView(VerticalScroll):
    """Terminal view component"""

    DEFAULT_CSS = """
    TerminalView {
        padding: 1 2;
    }

    TerminalView Static {
    }

    TerminalView Static.muted {
        color: $text-muted;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def write(self, text: str, muted: bool = False) -> None:
        """Add output to terminal"""
        item = Static(text, classes=f"{'muted' if muted else ''}")
        self.mount(item)
        self.scroll_end(animate=True)
