from live_gold_api import get_gold_price, analyze_gold
from news_sentiment import fetch_gold_news, analyze_news_sentiment
from report_generator import generate_gold_report
from telegram_notify import send_telegram_message
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def run_daily_report():
    data = get_gold_data()
    analysis = analyze_gold(data)

    sentiment_label, sentiment_score = get_news_sentiment()

    message = build_trader_grade_report_md(
        analysis,
        sentiment_label,
        sentiment_score
    )

    send_telegram_message(message, parse_mode="Markdown")
