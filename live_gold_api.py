import yfinance as yf

def get_gold_price():
    fallback_current, fallback_previous = 4200, 4195
    try:
        gold = yf.Ticker("GC=F")  # COMEX gold futures
        data = gold.history(period="5d")
        if data.empty or len(data['Close']) < 2:
            raise ValueError("No gold price data returned")
        current_price = data['Close'][-1]
        previous_price = data['Close'][-2]
        print(f"Fetched gold prices: Current={current_price}, Previous={previous_price}")
        return current_price, previous_price
    except Exception as e:
        print(f"Error fetching gold price: {e}")
        return fallback_current, fallback_previous

def analyze_gold(current_price, previous_price):
    change_pct = (current_price - previous_price) / previous_price * 100
    if change_pct > 0.5:
        return "buy", 85, f"Gold is up {change_pct:.2f}% — bullish momentum."
    elif change_pct < -0.5:
        return "sell", 80, f"Gold is down {abs(change_pct):.2f}% — bearish momentum."
    else:
        return "hold", 70, f"Gold is stable ({change_pct:.2f}% change) — neutral outlook."
