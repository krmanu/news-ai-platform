import requests
from utils.database import news_collection
from utils.sentiment import analyze_sentiment
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

CURRENTS_API_KEY = os.getenv("CURRENTS_API_KEY")
SEARCH_URL = "https://api.currentsapi.services/v1/search"

# UI Name -> API Category

CATEGORY_MAP = {
    "Sports":     "sports",        # fix: was "sport"
    "Business":   "business",      # fix: was "economy_business_finance"
    "Technology": "technology",    # fix: was "science_technology"
    "Cinema":     "entertainment", # fix: was "arts_culture_entertainment"
    "Politics":   "politics",      # fix: was "politics_government"
}

# UI Name -> Country Code
COUNTRY_MAP = {
    "India":     "India",
    "America":   "USA America",
    "China":     "China",
    "Australia": "Australia",
    "UK":        "UK Britain",
    "Germany":   "Germany",
    "France":    "France",
    "Japan":     "Japan",
    "Brazil":    "Brazil",
    "Canada":    "Canada",
}

# Fetch Single Category News
def fetch_single(ui_category, cat_keyword, country_name, country_keyword):
    
    results = []
    try:
        headers = {"Authorization": CURRENTS_API_KEY}
        # API request parameters
        params = {
            "keywords":  f"{cat_keyword} {country_keyword}",  # fix: keyword search
            "language":  "en",
            "page_size": 10,
        }
         
        # Send request to CurrentsAPI
        response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=10)

        # Convert JSON response -> Python dictionary
        data = response.json()

        # Get all articles
        articles = data.get("news", [])

        for article in articles:
            title = article.get("title", "")

            if not title or title == "[Removed]":
                continue

            sentiment = analyze_sentiment(title)

            # MongoDB document
            news_data  = {
                "title": title,
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "source": article.get("author", "Unknown"),
                "category":ui_category,
                "country":country_name,
                "sentiment": sentiment,
                "publishedAt": article.get("published", ""),
                "summary": None,
                "fetchedAt":datetime.utcnow()
            }
            # Save in MongoDB
            news_collection.update_one({"url": article["url"]},{"$set": news_data},upsert=True)
            results.append(title)
        print(f" {country_name}/{ui_category}: {len(results)} articles")

    except Exception as e:
        print(f" CurrentsAPI error {country_name}/{ui_category}: {e}")

    return results

def fetch_all_news(country_name="India"):
    
    country_code = COUNTRY_MAP.get(country_name, "India")
    total = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(
                fetch_single,
                ui_cat, api_cat,
                country_code, country_name
            ): ui_cat
            for ui_cat, api_cat in CATEGORY_MAP.items()
        }
        for future in as_completed(futures):
            results = future.result()
            total += len(results)
    print(f"🎯 fetch_all_news total saved: {total}")
    return total