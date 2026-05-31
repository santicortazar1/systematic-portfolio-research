import pandas as pd
import numpy as np
import os

print("Starting macro regime analysis...")

# --- PATHS ---
portfolio_path = "data/processed/portfolio_returns.csv"
yield_path = "data/raw/yield_data.csv"  # you will create this
output_path = "data/processed/regime_metrics.csv"

# --- LOAD DATA ---
portfolios = pd.read_csv(portfolio_path, index_col=0, parse_dates=True)
yields = pd.read_csv(yield_path, index_col=0, parse_dates=True)

# --- COMPUTE SPREAD ---
yields.rename(columns={"T10Y2Y": "spread"}, inplace=True)

# --- CLASSIFY REGIME ---
yields["regime"] = np.where(yields["spread"] < 0, "Inversion", "Normal")

# --- RESAMPLE TO MONTHLY (ALIGN WITH RETURNS) ---
yields_monthly = yields.resample("ME").last()

# --- MERGE ---
data = portfolios.merge(yields_monthly[["spread", "regime"]], left_index=True, right_index=True, how="inner")

print("\n--- DATA CHECK ---")
print(data.head())

# --- METRICS FUNCTION (REUSE LOGIC) ---
periods_per_year = 12
epsilon = 1e-8

def compute_metrics(r):
    r = r.dropna()
    if len(r) < 5:
        return None

    cumulative = (1 + r).prod()
    n = len(r)

    cagr = cumulative ** (periods_per_year / n) - 1
    vol = r.std() * np.sqrt(periods_per_year)

    sharpe = np.nan if vol < epsilon else (r.mean() / r.std()) * np.sqrt(periods_per_year)

    downside = r[r < 0]
    downside_std = downside.std() * np.sqrt(periods_per_year) if len(downside) > 0 else np.nan
    sortino = np.nan if downside_std < epsilon else (r.mean() * periods_per_year) / downside_std

    cum = (1 + r).cumprod()
    peak = cum.cummax()
    dd = (cum - peak) / peak
    max_dd = dd.min()

    return {
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_dd
    }

# --- COMPUTE BY REGIME ---
results = []

for regime in ["Normal", "Inversion"]:
    subset = data[data["regime"] == regime]

    for col in ["Traditional", "Multifactor", "Defensive"]:
        metrics = compute_metrics(subset[col])

        if metrics:
            metrics["Portfolio"] = col
            metrics["Regime"] = regime
            results.append(metrics)

regime_df = pd.DataFrame(results)

# --- SAVE ---
os.makedirs("data/processed", exist_ok=True)
regime_df.to_csv(output_path, index=False)

print("\n--- REGIME METRICS ---")
print(regime_df)
print(f"\nSaved to {output_path}")