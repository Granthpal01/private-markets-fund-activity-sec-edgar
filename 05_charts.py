import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

# ── Load analysis results ──────────────────────────────────────────
quarterly = pd.read_csv("data/processed/quarterly_volume.csv")
strategy  = pd.read_csv("data/processed/strategy_breakdown.csv")
geo       = pd.read_csv("data/processed/geography.csv")
yoy       = pd.read_csv("data/processed/yoy_trend.csv")

strategy["TOTAL_RAISED_M"] = (pd.to_numeric(
    strategy["TOTAL_RAISED"], errors="coerce") / 1_000_000).round(0)

# ── Chart 1: Quarterly filing volume ──────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(quarterly["YEAR_QUARTER"], quarterly["FILINGS"],
       color="#1a3a6b", edgecolor="white")
ax.set_title("Private Fund Raise Activity — Quarterly Filing Volume (2023–2025)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Quarter")
ax.set_ylabel("Number of Form D Filings")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("outputs/01_quarterly_volume.png", dpi=150)
plt.close()
print("Chart 1 saved")

# ── Chart 2: Strategy breakdown — filings count ───────────────────
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#1a3a6b", "#c8a84b", "#2e7d32", "#c62828"]
ax.barh(strategy["INVESTMENTFUNDTYPE"], strategy["FILINGS"],
        color=colors, edgecolor="white")
ax.set_title("Filings by Strategy (2023–2025)", fontsize=13,
             fontweight="bold")
ax.set_xlabel("Number of Filings")
plt.tight_layout()
plt.savefig("outputs/02_strategy_filings.png", dpi=150)
plt.close()
print("Chart 2 saved")

# ── Chart 3: Strategy breakdown — capital raised ──────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(strategy["INVESTMENTFUNDTYPE"], strategy["TOTAL_RAISED_M"],
        color=colors, edgecolor="white")
ax.set_title("Total Capital Raised by Strategy $M (2023–2025)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Total Offering Amount ($M)")
plt.tight_layout()
plt.savefig("outputs/03_strategy_capital.png", dpi=150)
plt.close()
print("Chart 3 saved")

# ── Chart 4: Year over year trend ─────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(yoy["YEAR"].astype(str), yoy["FILINGS"],
       color="#1a3a6b", edgecolor="white", width=0.4)
for i, row in yoy.iterrows():
    if pd.notna(row["YOY_CHANGE_PCT"]):
        ax.text(i, row["FILINGS"] + 200,
                f"+{row['YOY_CHANGE_PCT']}%",
                ha="center", fontsize=11, color="#2e7d32",
                fontweight="bold")
ax.set_title("Year-over-Year Filing Volume (2023–2025)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Total Filings")
ax.set_ylim(0, yoy["FILINGS"].max() * 1.15)
plt.tight_layout()
plt.savefig("outputs/04_yoy_trend.png", dpi=150)
plt.close()
print("Chart 4 saved")

print("\nAll charts saved to outputs/")