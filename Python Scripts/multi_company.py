import requests
import time

API_KEY = "S92ZPCA54YY8HIIW"

symbols = ["AAPL", "MSFT", "NVDA"]

for symbol in symbols:

    print("Downloading:", symbol)

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"

    data = requests.get(url).json()

    print("Company:", data.get("Name"))

    print("-" * 50)

    time.sleep(1)