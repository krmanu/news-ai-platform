from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def verify_news_web(title: str):

    try:
        response = client.search(
            query=title,
            search_depth="basic",
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return ""

        return results[0]["content"]

    except Exception as e:
        print("Search error:", e)
        return ""