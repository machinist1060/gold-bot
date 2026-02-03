def generate_gold_report(price_outlook, news_events, futures_prices, sentiment, recommendation, sources):
    sources_md = "".join(f"- {s}\n" for s in sources)
    return f"""
# Gold Market Analysis Summary

## 1. Gold's Price Outlook
{price_outlook}

## 2. Coming News or Events That May Affect Gold's Price
{news_events}

## 3. Gold Futures Prices
{futures_prices}

## 4. Overall Market Sentiment
{sentiment}

---

## Recommendation
Based on the analysis, **I recommend that you {recommendation['action'].upper()} gold.**
{recommendation['reasoning']}

---

### Sources
{sources_md}
"""
