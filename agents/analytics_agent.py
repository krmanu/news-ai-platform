from utils.database import news_collection


def top_news_by_category(category, country):
    # Search matching news
    query = {
        "category": category,
        "country": country
    }

    # Fetch latest 10 news
    news = news_collection.find(query)
    news = news.sort("fetchedAt", -1)
    news = news.limit(10)

    # Convert Mongo cursor -> Python list
    return list(news)