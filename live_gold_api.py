def get_gold_data() -> pd.DataFrame:
    """
    Fetch last 7 days of gold prices.
    First try spot gold from Stooq (/XAUSD).
    Fallback to COMEX front-month futures (GC=F) if Stooq fails.
    """
    # 1️⃣ Try Stooq spot gold
    print("Trying spot gold via Stooq: /XAUSD")
    gold = yf.Ticker("/XAUSD")
    data = gold.history(period="7d", interval="1d").dropna()

    if data.empty or len(data) < 4:
        # 2️⃣ Fallback: COMEX front-month futures
        print("Stooq had no data — trying COMEX futures GC=F fallback")
        gold = yf.Ticker("GC=F")
        data = gold.history(period="7d", interval="1d", auto_adjust=False).dropna()

        if data.empty or len(data) < 4:
            raise ValueError("Insufficient gold price data returned")

    return data
