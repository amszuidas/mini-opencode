import asyncio
import datetime
import re

from langchain.messages import (
    AIMessage,
    AIMessageChunk,
    AnyMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Overwrite
from textual.app import App
from textual.widgets import TabbedContent

from mini_opencode import project
from mini_opencode.agents import create_coding_agent
from mini_opencode.cli.components import (
    ChatView,
    EditorTabs,
    TerminalView,
    TodoListView,
)
from mini_opencode.cli.history import HistoryManager
from mini_opencode.tools import load_mcp_tools


class AgentController:
    """Controller for managing the AI agent and its interactions."""

    def __init__(self, app: "App"):
        self.app = app
        self._coding_agent = None
        self._mcp_tools: list = []
        self._terminal_tool_calls: list[str] = []
        self._file_modification_tool_calls: dict[str, str] = {}
        self._checkpointer = MemorySaver()
        self._session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.history_manager = HistoryManager()

    @property
    def is_generating(self) -> bool:
        """Check if the agent is currently generating."""
        if hasattr(self.app, "is_generating"):
            return self.app.is_generating
        return False

    @is_generating.setter
    def is_generating(self, value: bool) -> None:
        """Set the generating state on the app."""
        if hasattr(self.app, "is_generating"):
            self.app.is_generating = value

    async def init_agent(self) -> None:
        """Initialize the agent and load tools."""
        terminal_view = self.app.query_one("#terminal-view", TerminalView)
        terminal_view.write("$ Loading MCP tools...")
        try:
            self._mcp_tools = await load_mcp_tools()
            tool_count = len(self._mcp_tools)
            if tool_count > 0:
                terminal_view.write(
                    f"- {tool_count} tool{' is' if tool_count == 1 else 's are'} loaded.\n",
                    True,
                )
            else:
                terminal_view.write("- No tools found.\n", True)
        except Exception:
            terminal_view.write("- Error loading tools.\n", True)

        terminal_view.write("$ Loading agent...")
        try:
            self._coding_agent = create_coding_agent(
                plugin_tools=self._mcp_tools, checkpointer=self._checkpointer
            )
            terminal_view.write("- Agent loaded successfully.\n", True)
            self.is_generating = False
            if hasattr(self.app, "focus_input"):
                self.app.focus_input()
        except Exception as e:
            # Fatal error, exit the application
            terminal_view.write(f"- Error loading agent: {e}\n", True)
            await asyncio.sleep(3)
            self.app.exit(1)

    async def handle_user_input(self, user_message: HumanMessage) -> None:
        """Handle user input and stream the response."""
        self.process_outgoing_message(user_message)
        self.is_generating = True
        try:
            current_ai_message: AIMessageChunk | None = None
            async for event_type, chunk in self._coding_agent.astream(
                {"messages": [user_message]},
                stream_mode=["messages", "updates"],
                config={"recursion_limit": 100, "thread_id": "thread_1"},
            ):
                if event_type == "messages":
                    if isinstance(chunk, Overwrite):
                        chunk = chunk.value
                    if isinstance(chunk, BaseMessage):
                        message_chunk = chunk
                    elif isinstance(chunk, (tuple, list)) and len(chunk) > 0:
                        message_chunk = chunk[0]
                    else:
                        continue

                    if isinstance(message_chunk, AIMessageChunk):
                        if current_ai_message is None:
                            current_ai_message = message_chunk
                            self.process_incoming_message(current_ai_message)
                        else:
                            current_ai_message += message_chunk
                            # During streaming, don't update tool call widgets to avoid partial parsing errors
                            self.update_incoming_message(
                                current_ai_message, update_tools=False
                            )

                elif event_type == "updates":
                    if isinstance(chunk, Overwrite):
                        chunk = chunk.value
                    if not isinstance(chunk, dict):
                        continue

                    roles = chunk.keys()
                    for role in roles:
                        node_output = chunk[role]
                        if node_output is None or not isinstance(node_output, dict):
                            continue

                        messages_value = node_output.get("messages", [])
                        if isinstance(messages_value, Overwrite):
                            messages_value = messages_value.value
                        if isinstance(messages_value, BaseMessage):
                            messages = [messages_value]
                        elif isinstance(messages_value, (list, tuple)):
                            messages = list(messages_value)
                        else:
                            continue

                        # Filter messages to only include those after the current user message.
                        # This prevents re-processing old messages if the node returns the full history.
                        user_idx = -1
                        for i, m in enumerate(messages):
                            if (
                                m.type == user_message.type
                                and m.content == user_message.content
                            ):
                                user_idx = i
                        new_messages = messages[user_idx + 1 :]

                        # Use a flag to track if we've handled the first AI message in this update
                        # by updating the currently streaming message.
                        first_ai_in_node = True
                        for message in new_messages:
                            if isinstance(message, AIMessage):
                                if first_ai_in_node and current_ai_message is not None:
                                    # Update with final message (includes complete tool calls)
                                    self.update_incoming_message(
                                        message, update_tools=True
                                    )
                                else:
                                    # Not added via streaming yet, or subsequent AI message in same node
                                    self.process_incoming_message(message)

                                first_ai_in_node = False
                                if message.tool_calls:
                                    self.process_tool_call_message(message)
                            elif isinstance(message, ToolMessage):
                                # Tool results are not streamed, add them normally
                                self.process_incoming_message(message)
                                self.process_tool_message(message)

                    # Node finished. Reset current_ai_message for next potential AI response
                    current_ai_message = None
        except Exception as e:
            error_message = AIMessage(
                content=f"❌ **An error occurred:** {str(e)}\n\nPlease try again."
            )
            self.process_incoming_message(error_message)
        finally:
            await self.save_current_history()
            self.is_generating = False
            if hasattr(self.app, "focus_input"):
                self.app.focus_input()

    def process_outgoing_message(self, message: HumanMessage) -> None:
        """Add user message to chat view."""
        chat_view = self.app.query_one("#chat-view", ChatView)
        chat_view.add_message(message)

    def process_incoming_message(self, message: AnyMessage) -> None:
        """Add AI or tool message to chat view."""
        chat_view = self.app.query_one("#chat-view", ChatView)
        chat_view.add_message(message)

    def update_incoming_message(
        self, message: AnyMessage, update_tools: bool = True
    ) -> None:
        """Update the last message in chat view."""
        chat_view = self.app.query_one("#chat-view", ChatView)
        chat_view.update_message(message, update_tools=update_tools)

    def process_tool_call_message(self, message: AIMessage) -> None:
        """Handle tool calls from the agent."""
        terminal_view = self.app.query_one("#terminal-view", TerminalView)
        todo_list_view = self.app.query_one("#todo-list-view", TodoListView)
        editor_tabs = self.app.query_one("#editor-tabs", EditorTabs)
        bottom_right_tabs = self.app.query_one("#bottom-right-tabs", TabbedContent)

        for tool_call in message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            preview = self._format_tool_call_preview(tool_name, tool_args)
            if tool_name in {"execute", "ls", "glob", "grep"}:
                self._terminal_tool_calls.append(tool_call["id"])
                terminal_view.write(preview or f"$ {tool_name}")
                bottom_right_tabs.active = "terminal-tab"
            elif tool_name == "write_todos":
                bottom_right_tabs.active = "todo-tab"
                todo_list_view.update_items(tool_args["todos"])
            elif tool_name == "read_file":
                editor_tabs.open_file(tool_args["file_path"])
            elif tool_name == "write_file":
                editor_tabs.open_file(tool_args["file_path"], tool_args.get("content"))
                self._file_modification_tool_calls[tool_call["id"]] = tool_args[
                    "file_path"
                ]
            elif tool_name == "edit_file":
                editor_tabs.open_file(tool_args["file_path"])
                self._file_modification_tool_calls[tool_call["id"]] = tool_args[
                    "file_path"
                ]

    def process_tool_message(self, message: ToolMessage) -> None:
        """Handle tool results."""
        terminal_view = self.app.query_one("#terminal-view", TerminalView)
        if message.tool_call_id in self._terminal_tool_calls:
            output = self._extract_code(message.content)
            terminal_view.write(
                output if output.strip() != "" else "\n(empty)\n",
                muted=True,
            )
            self._terminal_tool_calls.remove(message.tool_call_id)
        elif self._file_modification_tool_calls.get(message.tool_call_id):
            path = self._file_modification_tool_calls[message.tool_call_id]
            del self._file_modification_tool_calls[message.tool_call_id]
            editor_tabs = self.app.query_one("#editor-tabs", EditorTabs)
            editor_tabs.open_file(path)

    async def save_current_history(self) -> None:
        """Save the current session history."""
        if not self._coding_agent:
            return

        config = {"configurable": {"thread_id": "thread_1"}}
        try:
            state = await self._coding_agent.aget_state(config)
            messages = state.values.get("messages", [])
            if messages:
                self.history_manager.save_session(
                    messages, self._session_id, project_root=project.root_dir
                )
        except Exception:
            pass

    def _format_tool_call_preview(self, tool_name: str, tool_args: dict) -> str | None:
        """Format a tool call for the terminal view."""
        if tool_name == "execute":
            command = tool_args.get("command") or "unknown"
            return f"$ {command}"
        if tool_name == "ls":
            path = tool_args.get("path") or "."
            return f"$ ls {path}"
        if tool_name == "glob":
            pattern = tool_args.get("pattern") or "*"
            path = tool_args.get("path") or "/"
            return f"$ glob {pattern} {path}"
        if tool_name == "grep":
            pattern = tool_args.get("pattern") or "*"
            path = tool_args.get("path") or "."
            return f"$ grep {pattern} {path}"
        return None

    def _extract_code(self, text: str) -> str:
        """Extract code from a markdown block."""
        match = re.search(r"```(.*)```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text

    def clear_session(self) -> None:
        """Reset the agent session."""
        self._checkpointer = MemorySaver()
        self._coding_agent = create_coding_agent(
            plugin_tools=self._mcp_tools, checkpointer=self._checkpointer
        )
        self._terminal_tool_calls = []
        self._file_modification_tool_calls = {}
        self._session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    async def load_session(self, session_id: str, messages: list[AnyMessage]) -> None:
        """Load a previous session."""
        self._checkpointer = MemorySaver()
        self._coding_agent = create_coding_agent(
            plugin_tools=self._mcp_tools, checkpointer=self._checkpointer
        )

        config = {"configurable": {"thread_id": "thread_1"}}
        await self._coding_agent.aupdate_state(config, {"messages": messages})

        self._terminal_tool_calls = []
        self._file_modification_tool_calls = {}
        self._session_id = session_id
