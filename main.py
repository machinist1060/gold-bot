from live_gold_api import get_gold_price, analyze_gold
from news_sentiment import fetch_gold_news, analyze_news_sentiment
from report_generator import generate_gold_report
from telegram_notify import send_telegram_message
from email_notify import send_email
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def run_daily_report():
    # Gold prices
    current, previous = get_gold_price()
    action, confidence, trend_text = analyze_gold(current, previous)
    
    # News sentiment
    articles = fetch_gold_news()
    sentiment, sentiment_score = analyze_news_sentiment(articles)
    
    # Generate Markdown report
    generate_gold_report(current, previous, action, confidence, trend_text, sentiment, sentiment_score)
    
    # Send Telegram
    msg = f"*Gold Daily Report*\nAction: {action.upper()} ({confidence}% confidence)\n{trend_text}\nNews Sentiment: {sentiment} ({sentiment_score:.2f})"
    send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, msg)
    
    # Optional email
    send_email("Daily Gold Report", msg)

if __name__ == "__main__":
    run_daily_report()
