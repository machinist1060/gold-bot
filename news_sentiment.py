import os
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def fetch_gold_news():
    if not NEWSAPI_KEY:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "gold OR XAU OR 'precious metals'",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 10,
        "apiKey": NEWSAPI_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("articles", [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_news_sentiment(articles):
    sentiments = []
    for article in articles:
        text = (article.get("title","") + " " + article.get("description","")).strip()
        if text:
            sentiments.append(sia.polarity_scores(text)["compound"])
    if sentiments:
        avg = sum(sentiments)/len(sentiments)
        if avg >= 0.05: return "bullish", avg
        if avg <= -0.05: return "bearish", avg
    return "neutral", 0
