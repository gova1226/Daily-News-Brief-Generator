# app.py

import streamlit as st
import json
from datetime import date
from news_fetcher import collect_news
from summarizer import summarize
from utils import deduplicate_articles

st.set_page_config(page_title="Daily News Brief Generator", layout="wide")
st.title("🗞️ Daily News Brief Generator")

USERS_FILE = "users.json"

# -------------------------------
# User Storage
# -------------------------------
def load_users():
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


users = load_users()

# -------------------------------
# Login Sidebar
# -------------------------------
st.sidebar.title("🔐 User Login")
username = st.sidebar.text_input("Enter username")

if st.sidebar.button("Login"):
    if username not in users:
        users[username] = {"segments": ["Technology"]}
        save_users(users)
    st.session_state.user = username

if "user" not in st.session_state:
    st.info("Please login to continue")
    st.stop()

user = st.session_state.user
st.sidebar.success(f"Welcome, {user}")

# -------------------------------
# Navigation
# -------------------------------
page = st.sidebar.radio("Navigation", ["🏠 Home", "⚙️ Customize"])

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "🏠 Home":
    st.title("🗞️ Your Personalized Daily News Brief")
    today = str(date.today())

    for seg in users[user]["segments"]:
        st.markdown(f"### {seg} Highlights — {today}")

        articles = deduplicate_articles(collect_news(seg, today))

        if not articles:
            st.warning("No news available.")
            continue

        for art in articles[:5]:
            text = art.get("description") or art.get("title")
            summary = summarize(text)
            st.write("•", summary)

        st.caption("Sources: NewsAPI, GNews, BBC RSS")
        st.divider()

# -------------------------------
# CUSTOMIZE PAGE
# -------------------------------
else:
    st.title("⚙️ Customize Your News Brief")

    segments = st.multiselect(
        "Choose News Segments",
        ["Technology", "Business", "Sports", "Health", "Entertainment", "Politics"],
        default=users[user]["segments"]
    )

    selected_date = st.date_input("Select Date", date.today())
    reading_pref = st.radio("Reading Preference", ["Short", "Detailed"])

    col1, col2 = st.columns(2)
    with col1:
        generate = st.button("Generate Brief")
    with col2:
        refresh = st.button("🔄 Refresh")

    if generate or refresh:
        users[user]["segments"] = segments
        save_users(users)

        for seg in segments:
            st.markdown(f"### {seg} — {selected_date}")
            articles = deduplicate_articles(collect_news(seg, str(selected_date)))

            for art in articles[:5]:
                text = art.get("description") or art.get("title")
                summary = summarize(text, short=(reading_pref == "Short"))
                st.write("•", summary)

            st.divider()