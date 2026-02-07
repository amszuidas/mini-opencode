from textual.widgets import Static


class TodoListView(Static):
    """Todo list view component"""

    DEFAULT_CSS = """
    TodoListView {
        color: $text-muted;
        padding: 1 2;
    }
    """

    def on_mount(self) -> None:
        self.update("(No TODO found)")

    def update_items(self, items: list[dict]):
        if not items:
            self.update("(No TODO found)")
            return

        display = ""
        for item in items:
            if item["status"] == "in_progress":
                status = "\\[•]"
            elif item["status"] == "completed":
                status = "\\[x]"
            else:
                status = "\\[ ]"
            content = item.get("content") or ""
            display += f"{status} {content}\n"
        self.update(display)
