from langchain.messages import AIMessage, AnyMessage, ToolMessage
from textual.app import ComposeResult
from textual.containers import Vertical

from .chat_input import ChatInput
from .message_list_view import MessageListView


class ChatView(Vertical):
    """Complete chat interface with scrollable messages and input"""

    DEFAULT_CSS = """
    ChatView {
        width: 1fr;
        background: $surface;
        padding: 0;
    }
    """

    _is_generating = False

    @property
    def is_generating(self) -> bool:
        return self._is_generating

    @is_generating.setter
    def is_generating(self, value: bool) -> None:
        self._is_generating = value
        message_list = self.query_one("#message-list", MessageListView)
        message_list.is_generating = value

    def compose(self) -> ComposeResult:
        """Compose the chat interface"""
        yield MessageListView(id="message-list")
        yield ChatInput(
            id="chat-input", placeholder="Type a message and press Enter..."
        )

    def on_mount(self) -> None:
        """Initialize chat with welcome message"""
        self.add_message(
            AIMessage(content="Hello! I'm mini-OpenCode. How can I help you?")
        )

    def add_message(self, message: AnyMessage) -> None:
        """Add a message to the chat"""
        message_list = self.query_one("#message-list", MessageListView)
        if not isinstance(message, ToolMessage):
            message_list.add_message(message)

    def update_message(self, message: AnyMessage, update_tools: bool = True) -> None:
        """Update the last message in the chat"""
        message_list = self.query_one("#message-list", MessageListView)
        if not isinstance(message, ToolMessage):
            message_list.update_last_message(message, update_tools=update_tools)

    def focus_input(self) -> None:
        """Focus the input field"""
        chat_input = self.query_one("#chat-input", ChatInput)
        chat_input.focus()
