import requests

SYMBOLS = {
    "bitcoin":      "BTCUSDT",
    "ethereum":     "ETHUSDT",
    "solana":       "SOLUSDT",
    "bnb":          "BNBUSDT",
    "xrp":          "XRPUSDT",
    "doge":         "DOGEUSDT",
    "cardano":      "ADAUSDT",
    "avalanche":    "AVAXUSDT",
    "chainlink":    "LINKUSDT",
    "litecoin":     "LTCUSDT",
    "polygon":      "MATICUSDT",
    "tron":         "TRXUSDT",
    "internetcomp": "ICPUSDT",
    "near":         "NEARUSDT",
    "aptos":        "APTUSDT",
}

def fetch_prices():
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol={}"
    out = {}

    for name, symbol in SYMBOLS.items():
        try:
            r = requests.get(url.format(symbol), timeout=5)
            data = r.json()

            if "lastPrice" not in data:
                out[name] = {"error": "invalid symbol"}
                continue

            out[name] = {
                "price": float(data["lastPrice"]),
                "change": float(data["priceChangePercent"]),
            }
        except Exception as e:
            out[name] = {"error": str(e)}

    return out

if __name__ == "__main__":
    print(fetch_prices())
#{'bitcoin': {'price': 85542.38, 'change': -6.926}, 'ethereum': {'price': 2791.27, 'change': -7.723}, 'solana': {'price': 131.07, 'change': -8.311}, 'tether': {'price': 0.9993, 'change': -0.17}}