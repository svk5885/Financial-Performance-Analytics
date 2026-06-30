import requests
import pandas as pd

API_KEY = "S92ZPCA54YY8HIIW"

symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}"

data = requests.get(url).json()

company_data = {
    "Company Name": [data.get("Name")],
    "Sector": [data.get("Sector")],
    "Industry": [data.get("Industry")],
    "Market Cap": [data.get("MarketCapitalization")],
    "PE Ratio": [data.get("PERatio")],
    "Profit Margin": [data.get("ProfitMargin")]
}

df = pd.DataFrame(company_data)

print(df)

df.to_excel("data/apple_overview.xlsx", index=False)

print("Excel file created successfully!")