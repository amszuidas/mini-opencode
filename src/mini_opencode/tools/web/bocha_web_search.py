import os
import requests
from langchain.tools import tool
from mini_opencode.config import get_config_section

@tool("bocha_web_search")
def bocha_websearch_tool(query: str, count: int = 10) -> str:
    """
    Perform a web search using the Bocha Web Search API.

    Args:
        query: Search keywords or query string
        freshness: Time range filter for search results
        summary: Whether to include text summaries in results
        count: Number of search results to return

    Returns:
        Detailed search results including webpage title, URL, summary, site name, site icon, and last crawled date.
    """

    url = 'https://api.bochaai.com/v1/web-search'
    settings = get_config_section(["tools", "configs", "bocha_web_search"])
    api_key = settings.get("api_key")
    if not api_key:
        raise ValueError(
            "The `bocha_api_key` is not specified in the `tools/configs/bocha_web_search` section."
        )
    headers = {
        'Authorization': f'Bearer {api_key}',  # Replace with your actual API key
        'Content-Type': 'application/json'
    }
    data = {
        "query": query,
        "freshness": "noLimit",  # Time range filter for results
        "summary": True,  # Whether to return long text summaries
        "count": count
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        json_response = response.json()
        try:
            if json_response["code"] != 200 or not json_response["data"]:
                return f"Search API request failed, reason: {json_response.get('msg', 'Unknown error')}"

            webpages = json_response["data"]["webPages"]["value"]
            if not webpages:
                return "No relevant results found."

            formatted_results = ""
            for idx, page in enumerate(webpages, start=1):
                formatted_results += (
                    f"Reference: {idx}\n"
                    f"Title: {page['name']}\n"
                    f"URL: {page['url']}\n"
                    f"Summary: {page['summary']}\n"
                    f"Site Name: {page['siteName']}\n"
                    f"Site Icon: {page['siteIcon']}\n"
                    f"Last Crawled: {page['dateLastCrawled']}\n\n"
                )
            return formatted_results.strip()
        except Exception as e:
            return f"Search API request failed, reason: result parsing error - {str(e)}"
    else:
        return f"Search API request failed, status code: {response.status_code}, error: {response.text}"

if __name__ == "__main__":
    print(bocha_websearch_tool.invoke({"query": "今天北京的天气怎么样？", "count": 5}))