from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b")

def categorize_news(title):
    prompt = f"""
    Classify this news into one category:
    Sports
    Politics
    Cinema
    Technology
    Business
    International
    News:{title}
    Only return category name.
    """
    response = llm.invoke(prompt)
    return response.content.strip()