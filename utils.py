# Optimized utils.py

# -------------------------------
# Remove duplicate news articles
# -------------------------------
def deduplicate_articles(articles):
    seen = set()
    unique = []

    for art in articles:
        title = art.get("title", "").strip().lower()

        if title and title not in seen:
            seen.add(title)
            unique.append(art)

    return unique
