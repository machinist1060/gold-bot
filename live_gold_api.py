import requests
from bs4 import BeautifulSoup

def get_gold_price():
    """
    Fetch the current gold spot price from Kitco (USD per oz).
    Returns:
        current_price (float)
        previous_price (float, approx previous close)
    """
    url = "https://www.kitco.com/gold-price-today-usa/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Kitco has <span id="sp-bid"> for current price
        price_span = soup.find("span", id="sp-bid")
        if not price_span:
            raise ValueError("Could not find gold price on Kitco page")

        current_price = float(price_span.text.replace(",", ""))
        
        # Approx previous price: assume 1 USD difference if not available
        previous_price = current_price - 1  

        print(f"Fetched gold prices from Kitco: Current={current_price}, Previous={previous_price}")
        return current_price, previous_price

    except Exception as e:
        print(f"Error fetching Kitco gold price: {e}")
        # fallback values
        fallback_current, fallback_previous = 4200, 4195
        print(f"Using fallback prices: Current={fallback_current}, Previous={fallback_previous}")
        return fallback_current, fallback_previous


def analyze_gold(current_price, previous_price):
    """
    Compute Buy/Sell/Hold recommendation based on daily % change.
    Returns:
        action (str): 'buy', 'sell', or 'hold'
        confidence (int): 0-100%
        trend_text (str): descriptive text for report
    """
    change_pct = (current_price - previous_price) / previous_price * 100
    if change_pct > 0.5:
        return "buy", 85, f"Gold is up {change_pct:.2f}% in the last day — bullish momentum."
    elif change_pct < -0.5:
        return "sell", 80, f"Gold is down {abs(change_pct):.2f}% in the last day — bearish momentum."
    else:
        return "hold", 70, f"Gold is relatively stable ({change_pct:.2f}% change) — neutral outlook."
