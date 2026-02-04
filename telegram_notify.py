import os
import requests

def send_telegram_message(token, chat_id, message):
    if not token or not chat_id:
        print("Telegram token/chat_id not set; skipping")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload).raise_for_status()
        print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
