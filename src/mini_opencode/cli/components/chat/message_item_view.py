import json

from langchain.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    ToolCall,
    ToolMessage,
)
from textual.app import ComposeResult
from textual.widgets import Markdown, Static


class MessageItemView(Static):
    """Single message item in the chat"""

    DEFAULT_CSS = """
    MessageItemView {
        width: 100%;
        height: auto;
        padding: 1;
        content-align: left top;
    }

    MessageItemView .message-header {
        color: $text-muted;
        text-style: dim;
        width: 100%;
    }

    MessageItemView.tool_calls_only {
        padding: 0 1;
    }

    MessageItemView .tool_call {
        color: $text-muted;
        text-style: dim;
        width: 100%;
    }

    MessageItemView .margin_top_1.tool_call {
        margin-top: 1;
    }

    MessageItemView #markdown {
        padding: 0 1 0 3;
        margin: 0;
    }
    """

    def __init__(self, message: AnyMessage, display_header: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.add_class(message.type)
        self.display_header = display_header

    def compose(self) -> ComposeResult:
        """Compose the message item"""
        if self.display_header:
            header = None
            if isinstance(self.message, HumanMessage):
                header = "[bold cyan]👤 You[/bold cyan]"
            elif isinstance(self.message, AIMessage):
                header = "[bold green]🤖 mini-OpenCode[/bold green]"
            if header:
                yield Static(header, classes="message-header")

        text_content = self.message.content.strip() if self.message.content else ""
        final_action = (
            isinstance(self.message, AIMessage)
            and text_content != ""
            and (not self.message.tool_calls or len(self.message.tool_calls) == 0)
        )

        # For AIMessage, always yield a Markdown widget if it's not a ToolMessage
        # to support streaming content updates.
        if not isinstance(self.message, ToolMessage):
            yield Markdown(
                text_content,
                id="markdown",
                classes=f"message-content{' final' if final_action else ''}",
            )

        if isinstance(self.message, AIMessage):
            if self.message.tool_calls:
                if text_content == "" and not self.display_header:
                    self.add_class("tool_calls_only")
                yield from self._compose_tool_calls()

    def _compose_tool_calls(self) -> ComposeResult:
        """Compose tool calls for AIMessage"""
        if not isinstance(self.message, AIMessage) or not self.message.tool_calls:
            return

        text_content = self.message.content.strip() if self.message.content else ""
        for tool_call in self.message.tool_calls:
            margin_top = 0
            if text_content and tool_call == self.message.tool_calls[0]:
                margin_top = 1
            yield Static(
                self.render_tool_call(tool_call),
                classes=f"tool_call margin_top_{margin_top}",
            )

    def update_message(self, message: AnyMessage, update_tools: bool = True) -> None:
        """Update the message and its visual representation"""
        self.message = message
        text_content = self.message.content.strip() if self.message.content else ""

        try:
            markdown = self.query_one("#markdown", Markdown)
            markdown.update(text_content)
        except Exception:
            # If markdown wasn't created yet (e.g. for ToolMessage), skip
            pass

        # For tool calls, we refresh the tool calls section only if requested
        if (
            update_tools
            and isinstance(self.message, AIMessage)
            and self.message.tool_calls
        ):
            # Remove existing tool calls
            for child in self.query(".tool_call"):
                child.remove()

            # Mount new tool calls
            for tool_call in self.message.tool_calls:
                margin_top = 0
                if text_content and tool_call == self.message.tool_calls[0]:
                    margin_top = 1
                self.mount(
                    Static(
                        self.render_tool_call(tool_call),
                        classes=f"tool_call margin_top_{margin_top}",
                    )
                )

            if text_content == "" and not self.display_header:
                self.add_class("tool_calls_only")
            else:
                self.remove_class("tool_calls_only")

    def render_tool_call(self, tool_call: ToolCall) -> str:
        name = tool_call["name"]
        args = tool_call["args"]
        match name:
            case "write_todos":
                return "📌 Update to-do list"
            case "execute":
                command = args.get("command") or "unknown"
                return f"💻 Execute command: {command}"
            case "read_file":
                file_path = args.get("file_path") or "unknown"
                return f"👁️  Read file: {file_path}"
            case "write_file":
                file_path = args.get("file_path") or "unknown"
                return f"✏️  Write file: {file_path}"
            case "edit_file":
                file_path = args.get("file_path") or "unknown"
                return f"✏️  Edit file: {file_path}"
            case "ls":
                path = args.get("path") or "."
                return f"🗂️ List files: {path}"
            case "glob":
                pattern = args.get("pattern") or "*"
                path = args.get("path") or "/"
                return f"🔍 Glob files: {pattern} in {path}"
            case "grep":
                pattern = args.get("pattern") or "*"
                path = args.get("path") or "."
                return f"🔍 Grep files: {pattern} in {path}"
            case "web_search":
                query = args.get("query") or "unknown"
                return f"🔍 Web search: {query}"
            case "web_fetch":
                url = args.get("url") or "unknown"
                return f"🔍 Web fetch: {url}"
            case "task":
                subagent_type = args.get("subagent_type") or "unknown"
                return f"🤖 Call subagent: {subagent_type}"
            case _:
                return f"🛠️ Use MCP tool: {name}({json.dumps(args)})"
