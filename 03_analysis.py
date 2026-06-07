import pandas as pd
import os

# ── Load master dataset ────────────────────────────────────────────
master = pd.read_csv("data/processed/master_funds.csv", low_memory=False)
print(f"Loaded {len(master):,} filings")

# ── Analysis 1: Filing volume by quarter ──────────────────────────
quarterly = (master
             .groupby("YEAR_QUARTER")
             .size()
             .reset_index(name="FILINGS")
             .sort_values("YEAR_QUARTER"))

print("\n── Quarterly filing volume ───────────────────────────────")
print(quarterly.to_string(index=False))

# ── Analysis 2: Strategy breakdown ────────────────────────────────
# ── Analysis 2: Strategy breakdown ────────────────────────────────
# Convert to numeric first — some values are text or blank
master["TOTALOFFERINGAMOUNT"] = pd.to_numeric(
    master["TOTALOFFERINGAMOUNT"], errors="coerce"
)

strategy = (master
            .groupby("INVESTMENTFUNDTYPE")
            .agg(
                FILINGS=("ACCESSIONNUMBER", "count"),
                TOTAL_RAISED=("TOTALOFFERINGAMOUNT", "sum"),
                AVG_FUND_SIZE=("TOTALOFFERINGAMOUNT", "mean")
            )
            .sort_values("FILINGS", ascending=False)
            .reset_index())

# ── Analysis 3: Top 10 states by filing volume ────────────────────
geo = (master[master["STATEORCOUNTRY"].notna()]
       .groupby("STATEORCOUNTRY")
       .size()
       .reset_index(name="FILINGS")
       .sort_values("FILINGS", ascending=False)
       .head(10))

print("\n── Top 10 states ─────────────────────────────────────────")
print(geo.to_string(index=False))

# ── Analysis 4: Year over year ────────────────────────────────────
yoy = (master
       .groupby("YEAR")
       .agg(
           FILINGS=("ACCESSIONNUMBER", "count"),
           UNIQUE_FUNDS=("ENTITYNAME", "nunique")
       )
       .reset_index())

yoy["YOY_CHANGE_PCT"] = yoy["FILINGS"].pct_change().mul(100).round(1)

print("\n── Year over year ────────────────────────────────────────")
print(yoy.to_string(index=False))

# ── Save all results ──────────────────────────────────────────────
os.makedirs("data/processed", exist_ok=True)
quarterly.to_csv("data/processed/quarterly_volume.csv", index=False)
strategy.to_csv("data/processed/strategy_breakdown.csv", index=False)
geo.to_csv("data/processed/geography.csv", index=False)
yoy.to_csv("data/processed/yoy_trend.csv", index=False)

print("\nAll analysis files saved to data/processed/")

strategy["TOTAL_RAISED_M"] = (strategy["TOTAL_RAISED"] / 1_000_000).round(0)
strategy["AVG_FUND_SIZE_M"] = (strategy["AVG_FUND_SIZE"] / 1_000_000).round(1)

print("\n── Strategy breakdown ────────────────────────────────────")
print(strategy[["INVESTMENTFUNDTYPE", "FILINGS",
                 "TOTAL_RAISED_M", "AVG_FUND_SIZE_M"]].to_string(index=False))