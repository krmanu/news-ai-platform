from newsapi import NewsApiClient
from utils.database import news_collection
from utils.sentiment import analyze_sentiment
from datetime import datetime
import os

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

CATEGORY_MAP = {
    "Sports":     "sports",
    "Business":   "business",
    "Technology": "technology",
    "Cinema":     "entertainment",
    "Politics":   "general",
}

def fetch_all_news():
    """Fast fetch — no LLM calls, just store raw news"""
    total = 0
    for ui_category, api_category in CATEGORY_MAP.items():
        try:
            articles = newsapi.get_top_headlines(
                category=api_category,
                language="en",
                page_size=10
            )
            for article in articles.get("articles", []):
                title = article.get("title", "")
                if not title or title == "[Removed]":
                    continue

                sentiment = analyze_sentiment(title)

                data = {
                    "title":       title,
                    "description": article.get("description", ""),
                    "url":         article.get("url", ""),
                    "source":      article["source"]["name"],
                    "category":    ui_category,
                    "sentiment":   sentiment,
                    "publishedAt": article.get("publishedAt", ""),
                    "summary":     None,
                    "fetchedAt":   datetime.utcnow()
                }
                news_collection.update_one(
                    {"url": article["url"]},
                    {"$set": data},
                    upsert=True
                )
                total += 1
        except Exception as e:
            print(f"Error fetching {ui_category}: {e}")
    return total