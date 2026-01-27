from textual import events
from textual.message import Message
from textual.widgets import TextArea


class ChatInput(TextArea):
    """Custom input for chat with multi-line support"""

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    class NavigateSuggestion(Message):
        def __init__(self, direction: int) -> None:
            self.direction = direction
            super().__init__()

    class SelectSuggestion(Message):
        def __init__(self) -> None:
            super().__init__()

    DEFAULT_CSS = """
    ChatInput {
        dock: bottom;
        margin: 1 2;
        padding: 0 1;
        background: $boost;
        border: none;
        width: 100%;
        height: 5;
        overflow-y: auto;
    }

    ChatInput:focus {
        border: none;
        background: $boost;
    }
    """

    def __init__(self, *args, **kwargs):
        # Set default placeholder if not provided
        if "placeholder" not in kwargs:
            kwargs["placeholder"] = (
                "Input message or / for commands, Enter to send, Ctrl+J for newline"
            )
        super().__init__(*args, **kwargs)
        self.show_line_numbers = False
        self.soft_wrap = True
        self.suggestions_active = False

    def on_key(self, event: events.Key) -> None:
        """Handle key presses for submit and newline."""
        if event.key == "enter":
            if self.suggestions_active:
                self.post_message(self.SelectSuggestion())
                event.prevent_default()
                event.stop()
            else:
                self.action_submit()
                event.prevent_default()
                event.stop()
        elif event.key == "up" and self.suggestions_active:
            self.post_message(self.NavigateSuggestion(-1))
            event.prevent_default()
            event.stop()
        elif event.key == "down" and self.suggestions_active:
            self.post_message(self.NavigateSuggestion(1))
            event.prevent_default()
            event.stop()
        elif event.key == "ctrl+j":
            self.action_newline()
            event.prevent_default()
            event.stop()

    def action_submit(self) -> None:
        if self.text.strip():
            self.post_message(self.Submitted(self.text))
            self.text = ""

    def action_newline(self) -> None:
        self.insert("\n")
