from langchain.messages import AnyMessage
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll

from .loading_indicator import LoadingIndicator
from .message_item_view import MessageItemView


class MessageListView(VerticalScroll):
    """Scrollable message list container"""

    DEFAULT_CSS = """
    MessageListView {
        height: 1fr;
        padding: 1 0;
        background: $surface;
    }

    MessageListView #message-list {
        height: auto;
    }

    MessageListView.generating #loading {
        display: block;
    }

    MessageListView #loading {
        display: none;
        margin-left: 4;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_focus = True
        self.messages: list[AnyMessage] = []

    _is_generating = False

    @property
    def is_generating(self) -> bool:
        return self._is_generating

    @is_generating.setter
    def is_generating(self, value: bool) -> None:
        self._is_generating = value
        if value:
            self.add_class("generating")
        else:
            self.remove_class("generating")
        self.set_timer(0.1, self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> None:
        self.scroll_end(animate=True)

    def compose(self) -> ComposeResult:
        yield Vertical(id="message-list")
        yield LoadingIndicator(id="loading")

    def add_message(self, message: AnyMessage) -> None:
        """Add a new message to the list"""
        display_header = True
        if len(self.messages) == 0:
            display_header = True
        else:
            last_message = self.messages[-1]
            if last_message:
                if last_message.type == message.type:
                    display_header = False
        self.messages.append(message)
        message_item_view = MessageItemView(message, display_header=display_header)
        message_list = self.query_one("#message-list", Vertical)
        message_list.mount(message_item_view)
        self.set_timer(0.1, self._scroll_to_bottom)

    def update_last_message(self, message: AnyMessage, update_tools: bool = True) -> None:
        """Update the last message in the list"""
        if not self.messages:
            self.add_message(message)
            return

        self.messages[-1] = message
        message_list = self.query_one("#message-list", Vertical)
        if message_list.children:
            last_view = message_list.children[-1]
            if isinstance(last_view, MessageItemView):
                last_view.update_message(message, update_tools=update_tools)
        self.set_timer(0.1, self._scroll_to_bottom)
