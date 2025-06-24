from fastapi import FastAPI, Query
from pydantic import BaseModel
import feedparser
import requests
from typing import List, Optional
import os

app = FastAPI()

# In-memory reading list
reading_list = []

# Example tech RSS feeds
RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://www.theverge.com/rss/index.xml",
    "https://www.reddit.com/r/technology/.rss",
    "https://www.cnet.com/rss/news/",
    "https://www.engadget.com/rss.xml"
]

#add OpenAI config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-3.5-turbo"  # or another model if you prefer

class NewsRequest(BaseModel):
    query: str
    timeframe: Optional[str] = None  # e.g., '24h', 'week'
    max_articles: int = 5

class Article(BaseModel):
    title: str
    link: str
    summary: Optional[str] = None

def extract_keywords_with_ai(query: str) -> list:
    """Use OpenAI to extract keywords from a user query."""
    if not OPENAI_API_KEY:
        return []
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = (
        "Extract the main keywords (1-5 words) from this search query for news filtering. "
        "Return them as a comma-separated list, no explanations.\nQuery: " + query
    )
    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You extract keywords from user queries for news search."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 30
    }
    try:
        r = requests.post(OPENAI_URL, headers=headers, json=data, timeout=20)
        if r.ok:
            keywords = r.json()["choices"][0]["message"]["content"]
            return [k.strip() for k in keywords.split(",") if k.strip()]
    except Exception:
        pass
    return []

@app.post("/news", response_model=List[Article])
def get_news(req: NewsRequest):
    # Fetch articles from RSS feeds
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:req.max_articles]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")
            })
    # Use AI to extract keywords from the query
    keywords = extract_keywords_with_ai(req.query) if req.query else []
    # Filter by keywords if any
    if keywords:
        articles = [a for a in articles if any(k.lower() in a["title"].lower() or k.lower() in a["summary"].lower() for k in keywords)]
    # Summarize if requested
    if req.query and articles:
        prompt = f"Summarize these articles about '{req.query}':\n" + "\n".join([a["title"] + ": " + a["summary"] for a in articles])
        summary = openai_summarize(prompt)
        # Return summarized articles (for demo, just attach summary to first article)
        if summary:
            articles[0]["summary"] = summary
    return [Article(**a) for a in articles[:req.max_articles]]

def openai_summarize(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return "[OpenAI API key not set]"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200
    }
    try:
        r = requests.post(OPENAI_URL, headers=headers, json=data, timeout=30)
        if r.ok:
            return r.json()["choices"][0]["message"]["content"]
    except Exception:
        pass
    return ""

@app.post("/reading-list")
def save_to_reading_list(article: Article):
    reading_list.append(article.dict())
    return {"status": "saved"}

@app.get("/reading-list", response_model=List[Article])
def get_reading_list():
    return [Article(**a) for a in reading_list] 