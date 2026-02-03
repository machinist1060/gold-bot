import os
from report_generator import generate_gold_report
from live_gold_api import get_gold_price, analyze_gold
from news_sentiment import fetch_gold_news, analyze_news_sentiment
from telegram_notify import send_telegram_message
from email_notify import send_email

# --- Fetch live prices safely ---
try:
    current_price, previous_price = get_gold_price()
    action, confidence, trend_text = analyze_gold(current_price, previous_price)
except Exception as e:
    print(f"Error fetching live data: {e}")
    current_price, previous_price = 4200, 4195
    action, confidence, trend_text = "hold", 70, "Unable to fetch live data, using placeholder values."

# --- Fetch news sentiment ---
try:
    articles = fetch_gold_news()
    news_sentiment, sentiment_score = analyze_news_sentiment(articles)
    news_events = f"Recent news sentiment is {news_sentiment.upper()} (score: {sentiment_score:.2f})."
except Exception as e:
    print(f"Error fetching news: {e}")
    news_sentiment, sentiment_score = "neutral", 0
    news_events = "News sentiment unavailable; using neutral assumption."

# --- Adjust confidence based on news sentiment ---
if news_sentiment == "bullish" and action == "buy":
    confidence += 5
elif news_sentiment == "bearish" and action == "sell":
    confidence += 5
elif news_sentiment == "bullish" and action == "sell":
    confidence -= 5
elif news_sentiment == "bearish" and action == "buy":
    confidence -= 5

confidence = max(0, min(confidence, 100))  # clamp to 0-100%

# --- Fill report sections ---
price_outlook = f"Current gold price is ${current_price:.2f}. {trend_text}"
futures_prices = f"Previous close: ${previous_price:.2f}, Current: ${current_price:.2f}"
sentiment = f"Market sentiment suggests {action.upper()} with {confidence}% confidence."
recommendation = {
    "action": action,
    "reasoning": f"Based on live price movement and news sentiment, we recommend {action.upper()} gold. Confidence: {confidence}%"
}
sources = ["Live data via Yahoo Finance XAU/USD", "News via NewsAPI"]

# --- Generate Markdown report ---
os.makedirs("reports", exist_ok=True)
report_path = os.path.join("reports", "daily_gold_report.md")
report_md = generate_gold_report(price_outlook, news_events, futures_prices, sentiment, recommendation, sources)
with open(report_path, "w") as f:
    f.write(report_md)
print(f"Report generated: {report_path}")

# --- Send Telegram notification ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
summary_message = f"Gold Bot Daily Report:\nAction: {recommendation['action'].upper()}\nConfidence: {confidence}%\nCurrent Price: ${current_price:.2f}\nNews Sentiment: {news_sentiment.upper()}"
if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, summary_message)

# --- Send Email notification ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

email_body = f"""
Gold Bot Daily Report

Action: {recommendation['action'].upper()}
Confidence: {confidence}%
Current Price: ${current_price:.2f}
News Sentiment: {news_sentiment.upper()}

See dashboard for full Markdown report.
"""

if EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECIPIENT:
    send_email(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, "Gold Daily Report", email_body)
