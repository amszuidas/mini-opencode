from datetime import datetime

from langchain.tools import tool


@tool("get_today_date")
def get_today_date_tool() -> str:
    """
    Get the current date in YYYY-MM-DD format.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"Today's date is {today}."
