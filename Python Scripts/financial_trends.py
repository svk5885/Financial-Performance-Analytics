import requests
import pandas as pd

API_KEY = "S92ZPCA54YY8HIIW"

symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}"

data = requests.get(url).json()

reports = data["annualReports"]

financial_data = []

for report in reports:

    financial_data.append({
        "Fiscal Year": report.get("fiscalDateEnding"),
        "Revenue": report.get("totalRevenue"),
        "Gross Profit": report.get("grossProfit"),
        "Net Income": report.get("netIncome")
    })

df = pd.DataFrame(financial_data)

df["Revenue"] = pd.to_numeric(df["Revenue"])
df["Gross Profit"] = pd.to_numeric(df["Gross Profit"])
df["Net Income"] = pd.to_numeric(df["Net Income"])

df["Profit Margin %"] = (df["Net Income"] / df["Revenue"]) * 100

df["Gross Margin %"] = (
    df["Gross Profit"] / df["Revenue"]
) * 100

df["Previous Revenue"] = df["Revenue"].shift(-1)

df["Revenue Growth %"] = (
    (df["Revenue"] - df["Previous Revenue"])
    / df["Previous Revenue"]
) * 100

df["Previous Net Income"] = df["Net Income"].shift(-1)

df["Net Income Growth %"] = (
    (df["Net Income"] - df["Previous Net Income"])
    / df["Previous Net Income"]
) * 100

print(df.head())


print(df.dtypes)

df.to_excel("data/apple_financial_trends.xlsx", index=False)

print("Financial dataset created successfully!")