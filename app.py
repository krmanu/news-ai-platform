import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from agents.supervisor_agent import run_workflow
from utils.scheduler import start_scheduler

# Start background scheduler (fetches news every 30 min)
start_scheduler()

st.set_page_config(
    page_title="AI News Intelligence Platform",
    page_icon="🗞️",
    layout="wide"
)

st.title("🗞️ AI News Intelligence Platform")
st.caption("Powered by Agentic AI · MCP · Groq · MongoDB")

# Sidebar info
with st.sidebar:
    st.header("📌 About")
    st.markdown("Real-time news aggregation with AI summaries and MCP web verification.")
    st.divider()
    st.markdown("**Stack**")
    st.markdown("- LangChain + Groq LLM")
    st.markdown("- MCP DuckDuckGo Search")
    st.markdown("- MongoDB Atlas")
    st.markdown("- APScheduler (30 min refresh)")
    st.divider()
    st.caption("Your Name | github.com/yourname")  # 👈 update this

# Category selector
category = st.selectbox(
    "📂 Select Category",
    ["Sports", "Politics", "Cinema", "Technology", "Business"],
    index=0
)

# Auto-load on category change using session state
if "last_category" not in st.session_state:
    st.session_state.last_category = None
if "news_data" not in st.session_state:
    st.session_state.news_data = []

# Load when category changes OR first visit
if st.session_state.last_category != category:
    st.session_state.last_category = category
    st.session_state.news_data = []  # clear old results

    with st.spinner(f"Loading top {category} news..."):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            news = loop.run_until_complete(run_workflow(category))
            loop.close()
            st.session_state.news_data = news
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display news
news = st.session_state.news_data

if not news:
    st.info("No news found. Please check back in a moment — news is being fetched automatically.")
else:
    st.success(f"Showing top {len(news)} news for **{category}**")
    st.divider()

    for i, item in enumerate(news):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader(f"{i+1}. {item['title']}")
        with col2:
            if item.get("web_verified"):
                st.success("✅ Verified")
            else:
                st.warning("⚠️ Unverified")

        st.write(item.get("summary") or item.get("description") or "")

        if item.get("web_context"):
            with st.expander("🌐 MCP Web Context"):
                st.write(item["web_context"])

        col3, col4, col5 = st.columns(3)
        with col3:
            s = item.get("sentiment", "Neutral")
            emoji = "😊" if s == "Positive" else "😞" if s == "Negative" else "😐"
            st.write(f"**Sentiment:** {emoji} {s}")
        with col4:
            st.write(f"**Source:** {item.get('source', 'N/A')}")
        with col5:
            if item.get("url"):
                st.link_button("Read More 🔗", item["url"])

        st.divider()