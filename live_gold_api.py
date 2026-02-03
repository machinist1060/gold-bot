import yfinance as yf

def get_gold_price():
    gold = yf.Ticker("XAUUSD=X")
    data = gold.history(period="5d")
    if data.empty or len(data['Close']) < 2:
        raise ValueError("No gold price data returned from Yahoo Finance")
    return data['Close'][-1], data['Close'][-2]

def analyze_gold(current_price, previous_price):
    change_pct = (current_price - previous_price) / previous_price * 100
    if change_pct > 0.5:
        return "buy", 85, f"Gold is up {change_pct:.2f}% in the last day — bullish momentum."
    elif change_pct < -0.5:
        return "sell", 80, f"Gold is down {abs(change_pct):.2f}% in the last day — bearish momentum."
    else:
        return "hold", 70, f"Gold is relatively stable ({change_pct:.2f}% change) — neutral outlook."
