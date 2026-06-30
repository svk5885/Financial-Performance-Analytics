import requests
import pandas as pd
import time

API_KEY = "S92ZPCA54YY8HIIW"

symbols = ["AAPL", "MSFT", "NVDA"]

companies = []

for symbol in symbols:

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"

    data = requests.get(url).json()

    companies.append({
        "Symbol": symbol,
        "Company Name": data.get("Name"),
        "Sector": data.get("Sector"),
        "Industry": data.get("Industry"),
        "Market Cap": data.get("MarketCapitalization"),
        "PE Ratio": data.get("PERatio"),
        "Profit Margin": data.get("ProfitMargin")
    })

    time.sleep(1)

df = pd.DataFrame(companies)

print(df)

df.to_excel("data/company_overview.xlsx", index=False)

print("Excel file created successfully!")