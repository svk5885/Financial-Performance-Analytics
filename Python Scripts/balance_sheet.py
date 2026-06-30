import requests
import pandas as pd

API_KEY = "6QXWB1D0K34AFJ6F"

symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}"

response = requests.get(url)

data = response.json()

# Debugging check
if "annualReports" not in data:
    print("API Error:")
    print(data)
    exit()

reports = data["annualReports"]

balance_data = []

for report in reports:

    balance_data.append({
        "Fiscal Year": report.get("fiscalDateEnding"),
        "Total Assets": report.get("totalAssets"),
        "Total Liabilities": report.get("totalLiabilities"),
        "Total Shareholder Equity": report.get("totalShareholderEquity"),
        "Cash": report.get("cashAndCashEquivalentsAtCarryingValue")
    })

df = pd.DataFrame(balance_data)

# Convert numeric columns
df["Total Assets"] = pd.to_numeric(df["Total Assets"])
df["Total Liabilities"] = pd.to_numeric(df["Total Liabilities"])
df["Total Shareholder Equity"] = pd.to_numeric(df["Total Shareholder Equity"])
df["Cash"] = pd.to_numeric(df["Cash"])

# KPI Calculations
df["Debt Ratio %"] = (
    df["Total Liabilities"]
    / df["Total Assets"]
) * 100

df["Equity Ratio %"] = (
    df["Total Shareholder Equity"]
    / df["Total Assets"]
) * 100

df["Cash Ratio %"] = (
    df["Cash"]
    / df["Total Assets"]
) * 100

print(df.head())

print("\nData Types:")
print(df.dtypes)

# Save Excel File
df.to_excel(
    "data/balance_sheet_trends.xlsx",
    index=False
)

print("\nBalance Sheet Dataset Created Successfully!")