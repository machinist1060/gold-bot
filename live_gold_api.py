# live_gold_api.py
import yfinance as yf
import pandas as pd

# ------------------------------
# Helper functions
# ------------------------------

def ema(series: pd.Series, span: int) -> pd.Series:
    """Compute Exponential Moving Average (EMA)."""
    return series.ewm(span=span, adjust=False).mean()

def signal_strength(change_pct: float) -> str:
    """Return signal strength based on percentage change."""
    abs_move = abs(change_pct)
    if abs_move < 0.3:
        return "Weak"
    elif abs_move < 0.8:
        return "Moderate"
    else:
        return "Strong"

def confidence_from_move(change_pct: float) -> int:
    """Return confidence % based on price move."""
    base = min(abs(change_pct) * 120, 90)  # scale to max 90%
    return int(max(60, base))  # minimum confidence 60%

# ------------------------------
# Core functions
# ------------------------------

def get_gold_data() -> pd.DataFrame:
    """
    Fetch last 7 days of spot gold prices (XAUUSD=X) at daily intervals.
    Returns a DataFrame with Open/High/Low/Close/Volume.
    """
    gold = yf.Ticker("XAUUSD=X")
    data = gold.history(period="7d", interval="1d").dropna()
    if len(data) < 4:
        raise ValueError("Insufficient gold price data returned")
    return data

def analyze_gold(data: pd.DataFrame) -> dict:
    """
    Analyze gold price data and return trader-grade signal information.
    Includes EMA-3 trend, signal strength, confidence, action, and emoji.
    """
    close = data["Close"]
    current = close.iloc[-1]
    previous = close.iloc[-2]

    change_pct = (current - previous) / previous * 100

    # Sanity check
    if abs(change_pct) > 3:
        raise ValueError(f"Unrealistic gold move detected: {change_pct:.2f}%")

    # Trend via 3-day EMA
    ema3 = ema(close, 3).iloc[-1]
    trend_up = current > ema3

    if change_pct > 0.4 and trend_up:
        action, emoji = "BUY", "📈"
    elif change_pct < -0.4 and not trend_up:
        action, emoji = "SELL", "📉"
    else:
        action, emoji = "HOLD", "🟡"

    return {
        "current": float(current),
        "previous": float(previous),
        "change_pct": change_pct,
        "ema3": float(ema3),
        "trend": "Uptrend" if trend_up else "Downtrend",
        "action": action,
        "emoji": emoji,
        "strength": signal_strength(change_pct),
        "confidence": confidence_from_move(change_pct),
    }

# ------------------------------
# Telegram Markdown report builder
# ------------------------------

def build_trader_grade_report_md(analysis: dict, sentiment_label: str, sentiment_score: float) -> str:
    """
    Build a Markdown-formatted trader-grade Telegram message including:
    - current price
    - previous close
    - daily % change
    - EMA trend
    - signal strength
    - action + emoji
    - confidence
    - news sentiment + emoji
    """
    sentiment_emoji = {
        "bullish": "🟢",
        "bearish": "🔴",
        "neutral": "🟡"
    }.get(sentiment_label.lower(), "⚪")

    return f"""*🪙 GOLD — Daily Trading Signal*

*Price:* `${analysis['current']:,.2f}`  
*Prev Close:* `${analysis['previous']:,.2f}`  
*Change:* `{analysis['change_pct']:+.2f}%`

*Trend:* {analysis['trend']} (EMA-3: `{analysis['ema3']:,.2f}`)  
*Signal Strength:* *{analysis['strength']}*

*Action:* *{analysis['action']}* {analysis['emoji']}  
*Confidence:* *{analysis['confidence']}%*

*News Sentiment:* *{sentiment_label.capitalize()}* {sentiment_emoji}  
_Score: {sentiment_score:.2f}_
"""
