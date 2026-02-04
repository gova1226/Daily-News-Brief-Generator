# Optimized news_fetcher.py

import requests
import feedparser
import streamlit as st
from datetime import datetime, timedelta

# Load API keys from Streamlit secrets
NEWS_API_KEY = st.secrets.get("NEWSAPI_KEY", "")
GNEWS_API_KEY = st.secrets.get("GNEWS_API_KEY", "")

# -------------------------------
# Helper: Safe HTTP GET
# -------------------------------
def safe_get(url, params=None, timeout=6):
    try:
        res = requests.get(url, params=params, timeout=timeout)
        if res.status_code == 200:
            return res.json()
        return {}
    except Exception:
        return {}

# -------------------------------
# Fetch from NewsAPI
# -------------------------------
def fetch_newsapi(segment, date):
    if not NEWS_API_KEY:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": segment,
        "from": date,
        "to": date,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY,
    }

    data = safe_get(url, params)
    return data.get("articles", [])

# -------------------------------
# Fetch from GNews
# -------------------------------
def fetch_gnews(segment, date):
    if not GNEWS_API_KEY:
        return []

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": segment,
        "from": date,
        "to": date,
        "lang": "en",
        "token": GNEWS_API_KEY,
    }

    data = safe_get(url, params)
    return data.get("articles", [])

# -------------------------------
# Fetch from BBC RSS feeds
# -------------------------------
def fetch_rss(segment):
    rss_map = {
        "Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "Sports": "https://feeds.bbci.co.uk/sport/rss.xml",
        "Health": "https://feeds.bbci.co.uk/news/health/rss.xml",
        "Entertainment": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "Politics": "https://feeds.bbci.co.uk/news/politics/rss.xml",
    }

    feed_url = rss_map.get(segment, "")
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "description": entry.get("summary", ""),
            "source": "BBC RSS"
        })

    return articles

# -------------------------------
# Combined Retrieval Function
# -------------------------------
@st.cache_data(show_spinner=False)
def collect_news(segment, date):
    articles = []

    # Primary APIs
    articles.extend(fetch_newsapi(segment, date))
    articles.extend(fetch_gnews(segment, date))

    # Fallback if too few
    if len(articles) < 5:
        articles.extend(fetch_rss(segment))

    return articles
