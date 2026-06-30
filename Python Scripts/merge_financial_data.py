import pandas as pd

# Read the three datasets
income_df = pd.read_excel("data/apple_financial_trends.xlsx")
balance_df = pd.read_excel("data/balance_sheet_trends.xlsx")
cashflow_df = pd.read_excel("data/cash_flow_trends.xlsx")

# Merge Income Statement + Balance Sheet
master_df = pd.merge(
    income_df,
    balance_df,
    on="Fiscal Year",
    how="left"
)

# Merge Cash Flow data
master_df = pd.merge(
    master_df,
    cashflow_df,
    on="Fiscal Year",
    how="left"
)

# Sort latest year first
master_df = master_df.sort_values(
    by="Fiscal Year",
    ascending=False
)

# Save the final dataset
master_df.to_excel(
    "data/master_financial_dataset.xlsx",
    index=False
)

print(master_df.head())
print("\nMaster Financial Dataset Created Successfully!")