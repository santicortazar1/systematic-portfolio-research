import pandas as pd
import os

print("Starting portfolio construction...")

# --- PATHS ---
returns_path = "data/processed/returns_monthly.csv"
output_path = "data/processed/portfolio_returns.csv"

# --- LOAD RETURNS ---
returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)

# --- DEFINE WEIGHTS ---

# Traditional
w_trad = {
    "ACWI": 0.60,
    "AGG": 0.40
}

# Multifactor
w_mf = {
    "USMV": 0.20,
    "QUAL": 0.20,
    "MTUM": 0.20,
    "AGG": 0.40
}

# Defensive
w_def = {
    "USMV": 0.30,
    "QUAL": 0.30,
    "AGG": 0.40
}

# Convert to Series
w_trad = pd.Series(w_trad)
w_mf = pd.Series(w_mf)
w_def = pd.Series(w_def)

# --- REBALANCING LOGIC (QUARTERLY) ---

def compute_portfolio_returns(returns, weights):
    weights = weights.reindex(returns.columns).fillna(0)

    portfolio_returns = []
    current_weights = weights.copy()

    for i in range(len(returns)):

        # Rebalance every 3 months (index-based)
        if i % 3 == 0:
            current_weights = weights.copy()

        # Portfolio return
        r = (returns.iloc[i] * current_weights).sum()
        portfolio_returns.append(r)

        # Drift
        current_weights = current_weights * (1 + returns.iloc[i])
        current_weights = current_weights / current_weights.sum()

    return pd.Series(portfolio_returns, index=returns.index)

# --- BUILD PORTFOLIOS ---
trad_returns = compute_portfolio_returns(returns, w_trad)
mf_returns = compute_portfolio_returns(returns, w_mf)
def_returns = compute_portfolio_returns(returns, w_def)

# --- COMBINE ---
portfolio_df = pd.DataFrame({
    "Traditional": trad_returns,
    "Multifactor": mf_returns,
    "Defensive": def_returns
})

# --- SAVE ---
os.makedirs("data/processed", exist_ok=True)
portfolio_df.to_csv(output_path)

print("\nPortfolio construction complete.")
print(portfolio_df.head())

print("\nPortfolio construction complete.")
print(portfolio_df.head())

print("\n--- SUMMARY ---")
print(portfolio_df.describe())