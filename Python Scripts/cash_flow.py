import requests
import pandas as pd

API_KEY = "6QXWB1D0K34AFJ6F"

symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={API_KEY}"

data = requests.get(url).json()

if "annualReports" not in data:
    print("API Error:")
    print(data)
    exit()

reports = data["annualReports"]

cash_flow_data = []

for report in reports:
    cash_flow_data.append({
        "Fiscal Year": report.get("fiscalDateEnding"),
        "Operating Cash Flow": report.get("operatingCashflow"),
        "Capital Expenditure": report.get("capitalExpenditures"),
        "Net Income": report.get("netIncome")
    })

df = pd.DataFrame(cash_flow_data)

df["Operating Cash Flow"] = pd.to_numeric(df["Operating Cash Flow"])
df["Capital Expenditure"] = pd.to_numeric(df["Capital Expenditure"])
df["Net Income"] = pd.to_numeric(df["Net Income"])

# Capital expenditure is usually reported as a negative value.
# Adding it gives the standard Free Cash Flow calculation.
df["Free Cash Flow"] = (
    df["Operating Cash Flow"]
    + df["Capital Expenditure"]
)

df["Cash Conversion Ratio %"] = (
    df["Operating Cash Flow"]
    / df["Net Income"]
) * 100

print(df.head())

df.to_excel(
    "data/cash_flow_trends.xlsx",
    index=False
)

print("\nCash Flow Dataset Created Successfully!")