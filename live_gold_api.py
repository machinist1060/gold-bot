import yfinance as yf

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def signal_strength(change_pct):
    abs_move = abs(change_pct)
    if abs_move < 0.3:
        return "Weak"
    elif abs_move < 0.8:
        return "Moderate"
    else:
        return "Strong"

def confidence_from_move(change_pct):
    base = min(abs(change_pct) * 120, 90)
    return int(max(60, base))


def get_gold_data():
    gold = yf.Ticker("XAUUSD=X")
    data = gold.history(period="7d", interval="1d").dropna()

    if len(data) < 4:
        raise ValueError("Insufficient gold data")

    return data


def analyze_gold(data):
    close = data["Close"]
    current = close.iloc[-1]
    previous = close.iloc[-2]

    change_pct = (current - previous) / previous * 100

    if abs(change_pct) > 3:
        raise ValueError(f"Unrealistic gold move: {change_pct:.2f}%")

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
