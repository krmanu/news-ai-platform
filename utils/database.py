from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["news_ai"]
news_collection = db["articles"]