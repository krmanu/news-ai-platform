from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
# Load .env
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b",api_key=os.getenv("GROQ_API_KEY"))

def summarize_news(text):
    prompt = f"Summarize this news in 3 lines max:\n{text}"
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return ""