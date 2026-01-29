from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Markdown, TabbedContent, TabPane

from .code_view import CodeView


class EditorTabs(TabbedContent):
    DEFAULT_CSS = """
    EditorTabs {
        height: 1fr;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_map: dict[str, EditorTab] = {}

    def open_file(self, path: str, file_text: str | None = None):
        tab = self._find_tab_by_path(path)
        if tab is None:
            tab = EditorTab(path)
            self.tab_map[path] = tab
            self.add_pane(tab)
        self.active = tab.id
        tab.update(file_text)
        return tab

    def open_welcome(self):
        tab = TabPane(title="Welcome", id="welcome-tab")
        welcome_text = None
        for parent in Path(__file__).resolve().parents:
            candidate = parent / "docs" / "welcome.md"
            if candidate.exists():
                welcome_text = candidate.read_text(encoding="utf-8")
                break
        if welcome_text is None:
            welcome_text = "Welcome to mini-OpenCode."
        markdown = Markdown(welcome_text, id="welcome-view")
        self.add_pane(tab)
        tab.mount(markdown)
        self.active = tab.id

    def _find_tab_by_path(self, path: str) -> EditorTab | None:
        return self.tab_map.get(path)

    def refresh_code_theme(self) -> None:
        for code_view in self.query(CodeView):
            code_view.update_code(code_view.code, code_view.file_path)

    def clear_tabs(self) -> None:
        """Clear all tabs except welcome"""
        self.tab_map = {}
        for pane in list(self.query(TabPane)):
            if pane.id != "welcome-tab":
                self.remove_pane(pane.id)
        self.active = "welcome-tab"


class EditorTab(TabPane):
    def __init__(self, path: str, **kwargs):
        title = extract_filename(path)
        tab_id = kwargs.pop("id", None) or make_tab_id(path)
        super().__init__(title=title, id=tab_id, **kwargs)
        self.path = path

    def compose(self) -> ComposeResult:
        yield CodeView(id="code-view")

    def update(self, file_text: str | None = None):
        code_view = self.query_one("#code-view", CodeView)
        if file_text is not None:
            code_view.update_code(file_text, self.path)
        else:
            try:
                with open(self.path, "r", encoding="utf-8") as file:
                    code = file.read()
                code_view.update_code(code, self.path)
            except OSError as e:
                code_view.update_code(f"Error opening {self.path}:\n{e}", self.path)
            except UnicodeDecodeError:
                # Fallback for files that might not be UTF-8, though we prefer UTF-8
                try:
                    with open(self.path, "r", encoding="gbk") as file:
                        code = file.read()
                    code_view.update_code(code, self.path)
                except Exception as e:
                    code_view.update_code(
                        f"Error decoding {self.path}:\n{e}", self.path
                    )


def extract_filename(path: str) -> str:
    _path = Path(path)
    return _path.name


def make_tab_id(path: str) -> str:
    import hashlib

    digest = hashlib.md5(path.encode("utf-8")).hexdigest()
    return f"file-{digest[:12]}"
