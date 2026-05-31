import yfinance as yf
import pandas as pd
import os

print("Starting data download...")

# --- PARAMETERS ---
tickers = ["ACWI", "USMV", "QUAL", "MTUM", "AGG"]
start_date = "2005-01-01"
end_date = "2024-12-31"

# --- DOWNLOAD DATA ---
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)

# --- VALIDATION ---
if data.empty:
    raise ValueError("Downloaded data is empty. Check tickers or connection.")

print("Data downloaded successfully.")

# --- EXTRACT PRICES ---
if isinstance(data.columns, pd.MultiIndex):
    if "Adj Close" in data.columns.get_level_values(0):
        adj_close = data["Adj Close"]
        print("Using 'Adj Close'")
    else:
        adj_close = data["Close"]
        print("Using 'Close' as proxy for adjusted prices")
else:
    adj_close = data.copy()
    print("Single-level columns detected")

# --- SAFELY FLATTEN (ONLY IF NEEDED) ---
if isinstance(adj_close.columns, pd.MultiIndex):
    adj_close.columns = adj_close.columns.get_level_values(1)

# --- CLEANING ---
adj_close = adj_close.sort_index()
adj_close = adj_close.dropna(how="all")

# --- DIAGNOSTICS ---
print("\n--- DATA CHECK ---")
print(adj_close.head())

print("\n--- MISSING VALUES PER ETF ---")
print(adj_close.isna().sum())

# --- ALIGN DATA (COMMON START DATE) ---
adj_close = adj_close.dropna()

print("\n--- AFTER ALIGNMENT ---")
print(adj_close.head())
print("Start date:", adj_close.index.min())

# --- SAVE ---
os.makedirs("data/raw", exist_ok=True)
output_path = "data/raw/market_data.csv"
adj_close.to_csv(output_path)

print(f"\nDownload complete. Data saved to {output_path}")