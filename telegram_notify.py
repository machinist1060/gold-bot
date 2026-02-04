# telegram_notify.py
import requests

def send_telegram_message(chat_id: str, token: str, message: str, parse_mode: str = "Markdown"):
    """
    Send a Telegram message via bot API.

    Args:
        chat_id (str): Telegram chat ID to send the message to.
        token (str): Telegram bot token.
        message (str): The message text (Markdown formatting supported).
        parse_mode (str, optional): Markdown/MarkdownV2/HTML. Defaults to "Markdown".

    Returns:
        dict: JSON response from Telegram API.

    Raises:
        Exception: If Telegram API returns an error.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Telegram send failed: {e}")

    return response.json()
