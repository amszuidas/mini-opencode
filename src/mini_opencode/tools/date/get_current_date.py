from datetime import datetime

from langchain.tools import tool


@tool("get_current_date")
def get_current_date_tool() -> str:
    """
    Get the current date in YYYY-MM-DD format.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"Current date is {current_date}."
