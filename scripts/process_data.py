import pandas as pd
import os

print("Starting processing...")

# --- PATHS ---
raw_path = "data/raw/market_data.csv"
processed_path = "data/processed/returns_monthly.csv"

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

# --- LOAD RAW DATA ---
if not os.path.exists(raw_path):
    raise FileNotFoundError(f"Raw file not found at {raw_path}")

df = pd.read_csv(raw_path, index_col=0, parse_dates=True)
print("Raw data loaded.")

# --- VALIDATE STRUCTURE ---
print("\nColumns:")
print(df.columns)

# --- CLEAN DATA ---
df = df.sort_index()
df = df.dropna(how="all")

# --- RESAMPLE TO MONTHLY ---
df_monthly = df.resample("ME").last()

# --- CALCULATE RETURNS ---
returns = df_monthly.pct_change().dropna()

# --- ENFORCE COLUMN ORDER ---
returns = returns[["ACWI", "USMV", "QUAL", "MTUM", "AGG"]]

# --- DIAGNOSTICS ---
print("\n--- RETURNS CHECK ---")
print(returns.head())

print("\n--- DATE RANGE ---")
print("Start:", returns.index.min())
print("End:", returns.index.max())

# --- SAVE ---
returns.to_csv(processed_path)

print(f"\nProcessing complete. Saved to {processed_path}")