from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))    # Create MongoDB connection
db = client["news_ai"]                               # Create/select database
news_collection = db["articles"]                     # Create/select collection