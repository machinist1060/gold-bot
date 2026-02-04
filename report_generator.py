import os

def generate_gold_report(current_price, previous_price, action, confidence, trend_text, sentiment, sentiment_score):
    report = f"""# Gold Market Analysis Summary

## 1. Gold's Price Outlook
Current gold price: ${current_price:.2f}, Previous: ${previous_price:.2f}.
Trend analysis: {trend_text}

## 2. News Sentiment
Sentiment: {sentiment} (score: {sentiment_score:.2f})

## 3. Recommendation
Based on price movement and news sentiment, the suggested action is **{action.upper()}** with {confidence}% confidence.
"""
    os.makedirs("reports", exist_ok=True)
    path = "reports/daily_gold_report.md"
    with open(path, "w") as f:
        f.write(report)
    print(f"Report generated: {path}")
