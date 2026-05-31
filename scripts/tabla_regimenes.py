import pandas as pd

# --- LOAD DATA ---
regime_df = pd.read_csv("data/processed/regime_metrics.csv")

# --- PIVOT TABLE ---
table = regime_df.pivot(index="Portfolio", columns="Regime")

# --- ORDENAR MÉTRICAS (opcional pero recomendable) ---
table = table[[
    ("CAGR", "Normal"), ("CAGR", "Inversion"),
    ("Volatility", "Normal"), ("Volatility", "Inversion"),
    ("Sharpe", "Normal"), ("Sharpe", "Inversion"),
    ("Sortino", "Normal"), ("Sortino", "Inversion"),
    ("Max Drawdown", "Normal"), ("Max Drawdown", "Inversion")
]]

# --- REDONDEAR ---
table = table.round(3)

# --- RENOMBRAR COLUMNAS (más limpio visualmente) ---
table.columns = [
    "CAGR (N)", "CAGR (I)",
    "Vol (N)", "Vol (I)",
    "Sharpe (N)", "Sharpe (I)",
    "Sortino (N)", "Sortino (I)",
    "MaxDD (N)", "MaxDD (I)"
]

# --- MOSTRAR ---
table_pct = table.copy()

# Convertir solo métricas que son porcentajes
for col in table_pct.columns:
    if "CAGR" in col or "Vol" in col or "MaxDD" in col:
        table_pct[col] = (table_pct[col] * 100).round(2)
    else:
        table_pct[col] = table_pct[col].round(2)

print("\n--- TABLA FINAL (FORMATO MIXTO) ---")
print(table_pct)

# --- GUARDAR (opcional) ---
table.to_csv("outputs/tabla_regimenes.csv")