# Private Markets Fund Activity Analysis — SEC EDGAR (2023–2025)

**Author:** Granth Pal
**Tools:** Python · Pandas · SQL (SQLite) · Tableau
**Data:** SEC EDGAR Form D Bulk Data Sets
**Dashboard:** [View Live on Tableau Public](https://public.tableau.com/app/profile/granth.pal/viz/PrivateMarketFunds/PrivateMarketsFundActivityDashboardSECEDGAR20232025)

---

## What This Project Does

Analyses 99,000+ SEC Form D filings from 2023–2025 to track private fund
raise activity across PE, VC, hedge fund, and private debt strategies.

Form D is one of the only mandatory public disclosures for private funds
raising capital under Regulation D. This project replicates the primary
data sourcing workflow used by alternative assets data platforms like Preqin.

---

## Key Findings

- Private fund raise activity grew 5.3% in 2024 and 6.4% in 2025
- Hedge funds dominate by filing count (29,767) and capital raised ($2T+)
- Private equity has the highest average fund size at $268M per fund
- Q1 is consistently the strongest quarter across all three years
- 68.2% of filings do not disclose fund size — filed as "indefinite"
- Linqto Liquidshares LLC filed 266 Form Ds in 2 years — flagged as
  a data quality anomaly requiring deduplication review

---

## Why Form D Has Limits — The Preqin Value Proposition

Form D tells you a fund exists and is raising capital.
It does NOT tell you: LP investors, fund performance (IRR/MOIC),
portfolio companies, or management fees.

This is precisely the gap that platforms like Preqin fill through
proprietary research — making this project a direct simulation of
their data sourcing methodology.

---

## Project Structure
├── 01_explore.py          # Single quarter exploration
├── 02_build_master.py     # Full 12-quarter pipeline
├── 03_analysis.py         # Business analysis
├── 04_sql_analysis.py     # SQL validation queries
├── 05_charts.py           # Python visualisations
├── data/processed/        # Cleaned CSVs and SQLite DB
└── outputs/               # Chart PNGs

---

## How to Reproduce

```bash
# 1. Download 12 quarters from SEC EDGAR
# https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets
# Extract each ZIP into data/raw/<quarter>/

# 2. Install dependencies
pip install pandas matplotlib

# 3. Run pipeline
python3 02_build_master.py
python3 03_analysis.py
python3 04_sql_analysis.py
python3 05_charts.py
```

---

## Data Quality Notes

- Amendments (D/A) included — represent ongoing fundraising activity
- TOTALOFFERINGAMOUNT = 0 for 68.2% of filings (GPs file as indefinite)
- E9 state code = non-US filers (8,788 filings) — international funds
- Duplicate detection query identified serial filers for review