import asyncio
import re

from langchain.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, TabbedContent, TabPane

from mini_opencode import project
from mini_opencode.agents import create_coding_agent
from mini_opencode.tools import load_mcp_tools

from .components import ChatView, EditorTabs, TerminalView, TodoListView
from .theme import DARK_THEME, LIGHT_THEME, is_dark_mode


class ConsoleApp(App):
    """The main application for mini-OpenCode."""

    TITLE = "mini-OpenCode"

    CSS = """
    Screen {
        layout: horizontal;
        background: $background;
    }

    Header {
        background: $primary;
        color: $foreground;
    }

    Footer {
        background: $surface;
        color: $secondary;
    }

    #left-panel {
        width: 3fr;
        background: $panel;
    }

    #right-panel {
        width: 4fr;
        background: $boost;
    }

    #editor-view {
        height: 70%;
    }

    #bottom-right-tabs {
        height: 30%;
        background: $panel;
    }

    #bottom-right-tabs TabPane {
        padding: 0;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    _coding_agent: CompiledStateGraph
    _checkpointer: MemorySaver

    _is_generating = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checkpointer = MemorySaver()
        self._coding_agent = create_coding_agent(checkpointer=self._checkpointer)

    @property
    def is_generating(self) -> bool:
        return self._is_generating

    @is_generating.setter
    def is_generating(self, value: bool) -> None:
        self._is_generating = value
        chat_view = self.query_one("#chat-view", ChatView)
        chat_view.is_generating = value
        chat_view.disabled = value

    def compose(self) -> ComposeResult:
        yield Header(id="header")
        with Vertical(id="left-panel"):
            yield ChatView(id="chat-view")
        with Vertical(id="right-panel"):
            yield EditorTabs(id="editor-tabs")
            with TabbedContent(id="bottom-right-tabs"):
                with TabPane(id="terminal-tab", title="Terminal"):
                    yield TerminalView(id="terminal-view")
                with TabPane(id="todo-tab", title="To-do"):
                    yield TodoListView(id="todo-list-view")
        yield Footer(id="footer")

    def focus_input(self) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        chat_view.focus_input()

    def on_mount(self) -> None:
        self.register_theme(DARK_THEME)
        self.register_theme(LIGHT_THEME)
        self.theme = "dark" if is_dark_mode() else "light"
        self.sub_title = project.root_dir
        self.focus_input()
        editor_tabs = self.query_one("#editor-tabs", EditorTabs)
        editor_tabs.open_welcome()

        asyncio.create_task(self._init_agent())
        self.set_interval(2.0, self._check_system_theme)

    def _check_system_theme(self) -> None:
        """Check and update the theme based on system settings."""
        new_theme = "dark" if is_dark_mode() else "light"
        if self.theme != new_theme:
            self.theme = new_theme

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not self.is_generating and event.input.id == "chat-input":
            user_input = event.value.strip()
            if user_input:
                if user_input == "exit" or user_input == "quit":
                    self.exit()
                    return
                event.input.value = ""
                user_message = HumanMessage(content=user_input)
                self._handle_user_input(user_message)

    async def _init_agent(self) -> None:
        terminal_view = self.query_one("#terminal-view", TerminalView)
        terminal_view.write("$ Loading MCP tools...")
        try:
            mcp_tools = await load_mcp_tools()
            tool_count = len(mcp_tools)
            if tool_count > 0:
                terminal_view.write(
                    f"- {tool_count} tool{' is ' if tool_count == 1 else 's are'} loaded.\n",
                    True,
                )
            else:
                terminal_view.write("No tools found.\n", True)
        except Exception as e:
            # Fatal error
            print(f"Error loading MCP tools: {e}")
            self.exit(1)
            return
        self._coding_agent = create_coding_agent(
            plugin_tools=mcp_tools, checkpointer=self._checkpointer
        )

    @work(exclusive=True, thread=False)
    async def _handle_user_input(self, user_message: HumanMessage) -> None:
        self._process_outgoing_message(user_message)
        self.is_generating = True
        async for chunk in self._coding_agent.astream(
            {"messages": [user_message]},
            stream_mode="updates",
            config={"recursion_limit": 100, "thread_id": "thread_1"},
        ):
            roles = chunk.keys()
            for role in roles:
                messages: list[AnyMessage] = chunk[role].get("messages", [])
                for message in messages:
                    self._process_incoming_message(message)
        self.is_generating = False
        self.focus_input()

    def _process_outgoing_message(self, message: HumanMessage) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        chat_view.add_message(message)

    def _process_incoming_message(self, message: AnyMessage) -> None:
        chat_view = self.query_one("#chat-view", ChatView)
        chat_view.add_message(message)
        if isinstance(message, AIMessage) and message.tool_calls:
            self._process_tool_call_message(message)
        if isinstance(message, ToolMessage):
            self._process_tool_message(message)

    _terminal_tool_calls: list[str] = []
    _mutable_text_editor_tool_calls: dict[str, str] = {}

    def _process_tool_call_message(self, message: AIMessage) -> None:
        terminal_view = self.query_one("#terminal-view", TerminalView)
        todo_list_view = self.query_one("#todo-list-view", TodoListView)
        editor_tabs = self.query_one("#editor-tabs", EditorTabs)
        bottom_right_tabs = self.query_one("#bottom-right-tabs", TabbedContent)
        for tool_call in message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            if tool_name == "bash":
                self._terminal_tool_calls.append(tool_call["id"])
                terminal_view.write(f"$ {tool_args['command']}")
                bottom_right_tabs.active = "terminal-tab"
            if tool_name == "tree":
                self._terminal_tool_calls.append(tool_call["id"])
                terminal_view.write(
                    f"$ tree {tool_args['path']}{f' --max-depth={tool_args["max_depth"]}' if tool_args.get('max_depth') else ''}"
                )
            elif tool_name == "grep":
                self._terminal_tool_calls.append(tool_call["id"])
                terminal_view.write(f"$ grep {' '.join(tool_args.values())}")
            elif tool_name == "ls":
                self._terminal_tool_calls.append(tool_call["id"])
                terminal_view.write(f"$ ls {' '.join(tool_args.values())}")
            elif tool_name == "todo_write":
                bottom_right_tabs.active = "todo-tab"
                todo_list_view.update_items(tool_args["todos"])
            elif tool_name == "text_editor":
                command = tool_args["command"]
                if command == "create":
                    editor_tabs.open_file(
                        tool_args["path"],
                        tool_args["file_text"],
                    )
                else:
                    editor_tabs.open_file(tool_args["path"])
                if command != "view":
                    self._mutable_text_editor_tool_calls[tool_call["id"]] = tool_args[
                        "path"
                    ]

    def _process_tool_message(self, message: ToolMessage) -> None:
        terminal_view = self.query_one("#terminal-view", TerminalView)
        if message.tool_call_id in self._terminal_tool_calls:
            output = self._extract_code(message.content)
            terminal_view.write(
                output if output.strip() != "" else "\n(empty)\n",
                muted=True,
            )
            self._terminal_tool_calls.remove(message.tool_call_id)
        elif self._mutable_text_editor_tool_calls.get(message.tool_call_id):
            path = self._mutable_text_editor_tool_calls[message.tool_call_id]
            del self._mutable_text_editor_tool_calls[message.tool_call_id]
            editor_tabs = self.query_one("#editor-tabs", EditorTabs)
            editor_tabs.open_file(path)

    def _extract_code(self, text: str) -> str:
        match = re.search(r"```(.*)```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text


app = ConsoleApp()

if __name__ == "__main__":
    app.run()
