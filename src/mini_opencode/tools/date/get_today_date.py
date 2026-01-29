from datetime import datetime

from langchain.tools import ToolRuntime, tool

from mini_opencode.tools.reminders import generate_reminders


@tool("get_today_date", parse_docstring=True)
def get_today_date_tool(
    runtime: ToolRuntime,
) -> str:
    """
    Get the current date in YYYY-MM-DD format.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    reminders = generate_reminders(runtime)
    return f"Today's date is {today}.{reminders}"
