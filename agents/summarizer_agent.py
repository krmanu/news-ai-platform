from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

def summarize_news(text):
    prompt = f"Summarize this news in 3 lines max:\n{text}"
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return ""