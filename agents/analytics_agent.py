from utils.database import news_collection

def top_news_by_category(category):
    news = list(
        news_collection.find(
            {"category": category}
        ).sort("fetchedAt", -1).limit(10)
    )
    return news