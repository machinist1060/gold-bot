# main.py
import os
from live_gold_api import get_gold_data, analyze_gold, build_trader_grade_report_md
from news_sentiment import fetch_gold_news, analyze_news_sentiment
from telegram_notify import send_telegram_message

# ------------------------------
# Environment Variables
# ------------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ------------------------------
# Daily report function
# ------------------------------
def run_daily_report():
    try:
        # 1️⃣ Fetch gold price data
        data = get_gold_data()

        # 2️⃣ Analyze gold for trader-grade signal
        analysis = analyze_gold(data)

        # 3️⃣ Fetch news sentiment
        news_articles = fetch_gold_news()
        sentiment_label, sentiment_score = analyze_news_sentiment(news_articles)

        # 4️⃣ Build Markdown Telegram message
        message = build_trader_grade_report_md(
            analysis,
            sentiment_label,
            sentiment_score
        )

        # 5️⃣ Send to Telegram
        send_telegram_message(
            chat_id=TELEGRAM_CHAT_ID,
            token=TELEGRAM_TOKEN,
            message=message,
            parse_mode="Markdown"
        )

        print("✅ Daily gold report sent successfully.")

    except Exception as e:
        print(f"❌ Failed to send daily gold report: {e}")

# ------------------------------
# Entrypoint
# ------------------------------
if __name__ == "__main__":
    run_daily_report()
