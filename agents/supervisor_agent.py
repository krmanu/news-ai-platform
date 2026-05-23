from agents.analytics_agent import top_news_by_category
from agents.summarizer_agent import summarize_news
from agents.web_search_agent import verify_news_web

from utils.database import news_collection

from concurrent.futures import ThreadPoolExecutor, as_completed

# Summarize Single News Article
def summarize_item(item):

    if not item.get("summary"):
        try:
            text = item["title"] + ". " + item.get("description", "")
            summary = summarize_news(text)
            item["summary"] = summary
            news_collection.update_one(
                {"url": item["url"]},
                {"$set": {"summary": summary}}
            )
        except Exception:
            item["summary"] = item.get("description", "No summary available.")
    return item
    
# Main Workflow Controller
async def run_workflow(category, country):
    news = top_news_by_category(category, country)

    # Auto fetch if DB empty
    if not news:
        from services.news_service import fetch_all_news
        fetch_all_news(country)
        news = top_news_by_category(category, country)

    if not news:
        return []

    # Parallel summarization — all articles at once
    summarized = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(summarize_item, item): item for item in news}
        for future in as_completed(futures):
            summarized.append(future.result())

    # MCP verification (sequential to avoid rate limits)
    for item in summarized:
        try:
            web_context = await verify_news_web(item["title"])
            item["web_verified"] = bool(web_context)
            item["web_context"] = web_context[:300] if web_context else ""
        except Exception:
            item["web_verified"] = False
            item["web_context"] = ""

    return summarized