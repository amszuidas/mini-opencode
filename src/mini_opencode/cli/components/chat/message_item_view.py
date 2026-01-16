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
                header = "[bold green]⌨️ mini-OpenCode[/bold green]"
            if header:
                yield Static(header, classes="message-header")
        text_content = self.message.content.strip() if self.message.content else ""
        final_action = (
            isinstance(self.message, AIMessage)
            and text_content != ""
            and (not self.message.tool_calls or len(self.message.tool_calls) == 0)
        )
        if (
            not isinstance(self.message, ToolMessage)
            and text_content is not None
            and text_content != ""
        ):
            yield Markdown(
                text_content,
                id="markdown",
                classes=f"message-content{' final' if final_action else ''}",
            )
        if isinstance(self.message, AIMessage):
            if self.message.tool_calls:
                if text_content == "" and not self.display_header:
                    self.add_class("tool_calls_only")
                for tool_call in self.message.tool_calls:
                    margin_top = 0
                    if text_content and tool_call == self.message.tool_calls[0]:
                        margin_top = 1
                    yield Static(
                        self.render_tool_call(tool_call),
                        classes=f"tool_call margin_top_{margin_top}",
                    )

    def render_tool_call(self, tool_call: ToolCall) -> str:
        name = tool_call["name"]
        args = tool_call["args"]
        match name:
            case "bash":
                return f"💻 Execute command: {args['command']}"
            case "todo_write":
                return "📌 Update to-do list"
            case "read":
                return f"👁️  Read file: {args['path']}"
            case "write":
                return f"✏️  Write file: {args['path']}"
            case "edit":
                return f"✏️  Edit file: {args['path']}"
            case "grep":
                path = args.get("path") or "."
                return f"🔍 Search files: {args['pattern']} in {path}"
            case "ls":
                match_str = f" with {args['match']}" if args.get("match") else ""
                return f"🗂️ List files: {args['path']}{match_str}"
            case "tree":
                path = args.get("path") or "."
                depth = (
                    f" --max-depth={args['max_depth']}" if args.get("max_depth") else ""
                )
                return f"🔍 Explore project structure: {path}{depth}"
            case "web_search":
                return f"🔍 Web search: {args['query']}"
            case "web_crawl":
                return f"🔍 Web crawl: {args['url']}"
            case _:
                return f"🛠️ Use MCP tool: {name}({json.dumps(args)})"
