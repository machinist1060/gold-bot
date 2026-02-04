def build_trader_grade_report_md(analysis, sentiment_label, sentiment_score):
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
parse_mode="Markdown"

