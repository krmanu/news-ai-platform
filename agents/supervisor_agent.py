from agents.analytics_agent import top_news_by_category
from agents.summarizer_agent import summarize_news
from agents.web_search_agent import verify_news_web
from utils.database import news_collection

async def run_workflow(category):
    news = top_news_by_category(category)

    # Auto fetch if DB empty for this category
    if not news:
        from services.news_service import fetch_all_news
        fetch_all_news()
        news = top_news_by_category(category)

    summarized_news = []
    for item in news:
        # Use cached summary if exists
        if not item.get("summary"):
            try:
                text = item["title"] + ". " + item.get("description", "")
                summary = summarize_news(text)
                item["summary"] = summary
                # Cache to MongoDB
                news_collection.update_one(
                    {"url": item["url"]},
                    {"$set": {"summary": summary}}
                )
            except Exception:
                item["summary"] = item.get("description", "No summary available.")

        # MCP web verification
        try:
            web_context = await verify_news_web(item["title"])
            item["web_verified"] = bool(web_context)
            item["web_context"] = web_context[:300] if web_context else ""
        except Exception:
            item["web_verified"] = False
            item["web_context"] = ""

        summarized_news.append(item)

    return summarized_news