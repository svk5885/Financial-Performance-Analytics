import requests

API_KEY = "S92ZPCA54YY8HIIW"

symbol = "AAPL"

url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}"

data = requests.get(url).json()

print(data)

print(data["annualReports"][0])
report = data["annualReports"][0]
print("Fiscal Year:", report.get("fiscalDateEnding"))
print("Revenue:", report.get("totalRevenue"))
print("Gross Profit:", report.get("grossProfit"))
print("Net Income:", report.get("netIncome"))