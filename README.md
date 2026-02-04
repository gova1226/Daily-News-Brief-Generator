🗞️ Daily News Brief Generator

A Streamlit-based web application that generates a personalized daily news brief by collecting articles from multiple sources and summarizing them using a Transformer-based NLP model.
Users can log in, choose their preferred news segments, select reading length, and get concise or detailed summaries for any date.

🚀 Features:

🔐 User Login System
Simple username-based login
User preferences stored locally in users.json

🧠 AI-Powered Summarization
Uses Hugging Face’s t5-small model
Supports Short and Detailed summaries

📰 Multi-Source News Aggregation
NewsAPI
GNews
BBC RSS feeds (fallback)

🧹 Duplicate Removal
Automatically removes duplicate articles based on title

⚙️ Customization Options
Choose news categories
Select date
Control summary length

⚡ Optimized Performance
Cached API calls
Cached ML model loading

🏗️ Project Structure
├── app.py               # Streamlit application entry point
├── news_fetcher.py      # Fetches news from APIs and RSS feeds
├── summarizer.py        # Text summarization using transformers
├── utils.py             # Utility functions (deduplication)
├── requirements.txt     # Python dependencies
├── users.json           # User preferences (auto-created)
└── README.md            # Project documentation

🛠️ Tech Stack
Frontend / App Framework: Streamlit
Backend: Python
NLP Model: Hugging Face Transformers (t5-small)
APIs: NewsAPI, GNews
RSS: BBC News RSS
ML Framework: PyTorch

🔑 API Keys Setup
This app uses Streamlit Secrets for API keys.
Create a file:
.streamlit/secrets.toml
Add:
NEWSAPI_KEY = "your_newsapi_key_here"
GNEWS_API_KEY = "your_gnews_api_key_here"

🔔 If API keys are missing, the app automatically falls back to BBC RSS feeds.

▶️ Running the App
streamlit run app.py
