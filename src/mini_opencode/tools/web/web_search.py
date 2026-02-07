import json
import warnings

from langchain.tools import tool

from mini_opencode.config import get_config_section

# Suppress warnings from langchain_tavily regarding Pydantic field shadowing
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")
from langchain_tavily import TavilySearch  # noqa: E402


@tool("web_search", parse_docstring=True)
def web_search_tool(query: str, max_results: int = 5) -> str:
    """
    Search the web for the given query using Tavily.

    Args:
        query: The search query to execute.
        max_results: The maximum number of search results to return. Defaults to 5.

    Returns:
        A JSON string containing the search results, including titles, urls, and content.
    """
    settings = get_config_section(["tools", "configs", "web_search"])
    if not settings:
        raise ValueError(
            "The `tools/configs/web_search` section in `config.yaml` is not found. "
            "Please check your configuration file."
        )

    api_key = settings.get("api_key")
    if not api_key:
        raise ValueError(
            "The `tavily_api_key` is not specified in the `tools/configs/web_search` section."
        )

    tool = TavilySearch(
        tavily_api_key=api_key,
        max_results=max_results,
    )

    # The tool returns a list of results, we convert it to JSON string for consistency
    results = tool.invoke(query)
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(web_search_tool.invoke({"query": "NBA Finals", "max_results": 5}))
