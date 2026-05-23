import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from agents.supervisor_agent import run_workflow
from utils.scheduler import start_scheduler
from services.news_service import COUNTRY_MAP

# Load Environment Variables
load_dotenv()

# Start Background Scheduler
start_scheduler()

st.set_page_config(
    page_title="AI News Intelligence Platform",
    page_icon="🗞️",
    layout="wide"
)

st.title("🗞️ AI News Intelligence Platform")
st.caption("Powered by Agentic AI · MCP · Groq · MongoDB")

with st.sidebar:
    st.header("📌 About")
    st.markdown("Real-time news platform with AI-powered summaries and live web verification.")
    st.divider()
    st.markdown("### ⚙️ Tech Stack")
    st.markdown("""
    - Groq LLM + LangChain
    - Tavily Web Search API
    - MongoDB Atlas
    - Parallel AI Summarization
    - APScheduler (Auto Refresh)
    - Streamlit Dashboard
    """)
    st.divider()
    st.markdown("### 🚀 Features")

    st.markdown("""
    - Real-time news aggregation
    - AI-generated summaries
    - Category-wise filtering
    - Web-verified news context
    - Fast parallel processing
    """)
    st.caption("Manohar K R | github.com/krmanu/news-ai-platform")

# Two dropdowns side by side
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox(
        "🌍 Select Country",
        list(COUNTRY_MAP.keys()),  # India, America, China... (no flags)
        index=0
    )
with col2:
    category = st.selectbox(
        "📂 Select Category",
        ["Sports", "Politics", "Cinema", "Technology", "Business"],
        index=0
    )

# Session state to avoid re-fetching same selection
cache_key = f"{country}_{category}"

if "cache_key" not in st.session_state:
    st.session_state.cache_key = None

if "news_data" not in st.session_state:
    st.session_state.news_data = []

if st.session_state.cache_key != cache_key:
    
    st.session_state.cache_key = cache_key
    st.session_state.news_data = []
    
    with st.spinner(f"Loading {category} news for {country}..."):

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            news = loop.run_until_complete(run_workflow(category, country))
            loop.close()
            st.session_state.news_data = news

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display
news = st.session_state.news_data

if not news:
    st.info(f"No news found for {country} → {category}.")
else:
    st.success(f"Top {len(news)} **{category}** news from **{country}**")
    st.divider()

    for i, item in enumerate(news):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader(f"{i+1}. {item['title']}")

        with col2:
            if item.get("web_verified"):
                st.success("Verified")
            else:
                st.warning("Unverified")

        st.write(item.get("summary") or item.get("description") or "")

        if item.get("web_context"):
            with st.expander("🌐 MCP Web Context"):
                st.write(item["web_context"])

        c1, c2, c3 = st.columns(3)
        with c1:
            s = item.get("sentiment", "Neutral")
            emoji = "😊" if s == "Positive" else "😞" if s == "Negative" else "😐"
            st.write(f"**Sentiment:** {emoji} {s}")

        with c2:
            st.write(f"**Source:** {item.get('source', 'N/A')}")

        with c3:
            if item.get("url"):
                st.link_button("Read More 🔗", item["url"])

        st.divider()