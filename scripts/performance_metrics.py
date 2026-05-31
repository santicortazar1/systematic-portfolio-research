import pandas as pd
import numpy as np
import os

print("Starting performance analysis...")

# --- PATHS ---
input_path = "data/processed/portfolio_returns.csv"
output_path = "data/processed/performance_metrics.csv"

# --- LOAD DATA ---
returns = pd.read_csv(input_path, index_col=0, parse_dates=True)

# --- PARAMETERS ---
rf_rate = 0.0
periods_per_year = 12
epsilon = 1e-8  # prevent division by zero

# --- METRICS FUNCTIONS ---

def CAGR(returns):
    cumulative = (1 + returns).prod()
    n_periods = len(returns)
    return cumulative ** (periods_per_year / n_periods) - 1


def annual_volatility(returns):
    return returns.std() * np.sqrt(periods_per_year)


def sharpe_ratio(returns):
    excess_returns = returns - rf_rate / periods_per_year
    vol = returns.std()
    if vol < epsilon:
        return np.nan
    return (excess_returns.mean() / vol) * np.sqrt(periods_per_year)


def sortino_ratio(returns):
    downside = returns[returns < 0]
    if len(downside) < 5:  # stability threshold
        return np.nan
    downside_std = downside.std()
    if downside_std < epsilon:
        return np.nan
    return (returns.mean() * periods_per_year) / (downside_std * np.sqrt(periods_per_year))


def max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()


def cumulative_return(returns):
    return (1 + returns).prod() - 1


# --- COMPUTE METRICS ---

results = {}

for col in returns.columns:
    r = returns[col].dropna()

    results[col] = {
        "CAGR": CAGR(r),
        "Total Return": cumulative_return(r),
        "Volatility": annual_volatility(r),
        "Sharpe": sharpe_ratio(r),
        "Sortino": sortino_ratio(r),
        "Max Drawdown": max_drawdown(r)
    }

metrics_df = pd.DataFrame(results).T

# --- CLEAN OUTPUT ---
metrics_df.replace([np.inf, -np.inf], np.nan, inplace=True)

# --- SAVE ---
os.makedirs("data/processed", exist_ok=True)
metrics_df.to_csv(output_path)

print("\n--- PERFORMANCE METRICS ---")
print(metrics_df)
print(f"\nSaved to {output_path}")