# AI News Intelligence Platform

## Overview

AI News Intelligence Platform is an agentic AI application that aggregates real-time news from multiple countries and categories, generates AI-powered summaries, performs sentiment analysis, verifies news using web search, and stores articles in MongoDB for fast retrieval.

The platform automatically refreshes news data using a background scheduler and provides users with a dashboard to explore the latest verified news.

## Features

* Real-time news aggregation from multiple countries
* Category-wise filtering
    * Sports
    * Politics
    * Technology
    * Business
    * Cinema
* AI-generated news summaries using Groq LLM
* Sentiment Analysis (Positive, Negative, Neutral)
* Tavily-powered web verification
* MongoDB news storage
* Automatic news refresh every 30 minutes
* Parallel processing for faster summarization
* Streamlit interactive dashboard

## Tech Stack

* Streamlit
* LangChain
* Groq LLM
* MongoDB Atlas
* Tavily Search API
* APScheduler
* TextBlob
* Python Asyncio
* Concurrent Futures

## Architecture

### News Collection Agent

* Fetches news from Currents API.
* Collects news across countries and categories.
* Stores articles in MongoDB.

### Sentiment Agent

* Analyzes article titles.
* Labels news as Positive, Negative, or Neutral.

### Summarization Agent

* Uses Groq LLM.
* Generates concise 3-line summaries.

### Verification Agent

* Uses Tavily Search.
* Searches the web for supporting information.
* Adds verification context to articles.

### Supervisor Agent

* Coordinates all agents.
* Executes summarization and verification workflows.
* Returns enriched news results to the UI.

## Workflow

1. Scheduler automatically fetches news every 30 minutes.
2. News articles are stored in MongoDB.
3. User selects a country and category.
4. Top articles are retrieved from MongoDB.
5. AI generates summaries.
6. Tavily verifies news through web search.
7. Dashboard displays:
    * Summary
    * Sentiment
    * Source
    * Verification Status
    * External News Link


## Key Highlights

* Multi-Agent AI Workflow
* Real-Time News Intelligence
* Web Verification using Tavily
* Automated Data Refresh
* Parallel AI Processing
* Country & Category Analytics
