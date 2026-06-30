import requests
import pandas as pd
import os
import time

# -----------------------------
# API Configuration
# -----------------------------
API_KEY = "6QXWB1D0K34AFJ6F"

companies = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA"
}

BASE_URL = "https://www.alphavantage.co/query"

# -----------------------------
# Fetch API Data
# -----------------------------
def get_financial_data(symbol, function_name):
    params = {
        "function": function_name,
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "annualReports" not in data:
        print(f"Could not fetch {function_name} data for {symbol}")
        print(data)
        return []

    return data["annualReports"]


# -----------------------------
# Convert API Value Safely
# -----------------------------
def convert_to_number(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# -----------------------------
# Extract and Combine Data
# -----------------------------
all_company_data = []

for symbol, company_name in companies.items():

    print(f"\nExtracting financial data for {company_name} ({symbol})...")

    income_reports = get_financial_data(symbol, "INCOME_STATEMENT")
    time.sleep(15)

    balance_reports = get_financial_data(symbol, "BALANCE_SHEET")
    time.sleep(15)

    # Store balance sheet reports by fiscal year
    balance_by_year = {
        report["fiscalDateEnding"][:4]: report
        for report in balance_reports
    }

    
    for income in income_reports:

        fiscal_year = income["fiscalDateEnding"][:4]

        # Keep only recent financial years
        if int(fiscal_year) < 2021:
            continue

        balance = balance_by_year.get(fiscal_year)

        if not balance:
            continue

        revenue = convert_to_number(income.get("totalRevenue"))
        gross_profit = convert_to_number(income.get("grossProfit"))
        net_income = convert_to_number(income.get("netIncome"))

        cash = convert_to_number(
            balance.get("cashAndCashEquivalentsAtCarryingValue")
        )

        total_assets = convert_to_number(balance.get("totalAssets"))
        total_liabilities = convert_to_number(balance.get("totalLiabilities"))
        shareholder_equity = convert_to_number(
            balance.get("totalShareholderEquity")
        )

        current_assets = convert_to_number(balance.get("totalCurrentAssets"))
        current_liabilities = convert_to_number(
            balance.get("totalCurrentLiabilities")
        )

        # -----------------------------
        # Calculated Metrics
        # -----------------------------
        profit_margin = (
            (net_income / revenue) * 100
            if revenue and net_income
            else None
        )

        
        current_ratio = (
            current_assets / current_liabilities
            if current_assets and current_liabilities
            else None
        )

        debt_to_equity = (
            total_liabilities / shareholder_equity
            if total_liabilities and shareholder_equity
            else None
        )

        # Add record
        all_company_data.append({
            "Company": company_name,
            "Ticker": symbol,
            "Fiscal Year": int(fiscal_year),

            "Revenue": revenue,
            "Gross Profit": gross_profit,
            "Net Income": net_income,

            "Cash and Cash Equivalents": cash,
            "Total Assets": total_assets,
            "Total Liabilities": total_liabilities,
            "Shareholder Equity": shareholder_equity,

            "Current Assets": current_assets,
            "Current Liabilities": current_liabilities,

            "Profit Margin %": profit_margin,
            "Revenue Growth %": None,
            "Current Ratio": current_ratio,
            "Debt to Equity Ratio": debt_to_equity
        })

        


# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(all_company_data)

# Sort data correctly
df = df.sort_values(
    by=["Company", "Fiscal Year"],
    ascending=[True, True]
)

# Calculate revenue growth after sorting by company and fiscal year
df["Revenue Growth %"] = (
    df.groupby("Company")["Revenue"]
      .pct_change() * 100
)

# Calculate Gross Margin %
df["Gross Margin %"] = (
    df["Gross Profit"] / df["Revenue"]
) * 100

# Calculate Return on Assets %
df["Return on Assets %"] = (
    df["Net Income"] / df["Total Assets"]
) * 100

# Round percentage and ratio columns
df["Profit Margin %"] = df["Profit Margin %"].round(2)
df["Revenue Growth %"] = df["Revenue Growth %"].round(2)
df["Current Ratio"] = df["Current Ratio"].round(2)
df["Debt to Equity Ratio"] = df["Debt to Equity Ratio"].round(2)
df["Gross Margin %"] = df["Gross Margin %"].round(2)
df["Return on Assets %"] = df["Return on Assets %"].round(2)

# -----------------------------
# Export to Excel
# -----------------------------
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    "company_financial_comparison.xlsx"
)

df.to_excel(output_file, index=False)

print("\nProject completed successfully.")
print(f"Excel file created: {output_file}")

print("\nPreview of dataset:")
print(df.head(10))