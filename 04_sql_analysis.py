import sqlite3
import pandas as pd

# ── Step 1: Load master CSV into a SQLite database ────────────────
master = pd.read_csv("data/processed/master_funds.csv", low_memory=False)
master["TOTALOFFERINGAMOUNT"] = pd.to_numeric(
    master["TOTALOFFERINGAMOUNT"], errors="coerce"
)

conn = sqlite3.connect("data/processed/funds.db")
master.to_sql("fund_filings", conn, if_exists="replace", index=False)
print(f"Loaded {len(master):,} rows into SQLite database")

# ── Query 1: Filing count by strategy and year ────────────────────
q1 = """
SELECT
    INVESTMENTFUNDTYPE,
    YEAR,
    COUNT(*) AS filings
FROM fund_filings
GROUP BY INVESTMENTFUNDTYPE, YEAR
ORDER BY INVESTMENTFUNDTYPE, YEAR
"""

print("\n── Query 1: Filings by strategy and year ─────────────────")
print(pd.read_sql_query(q1, conn).to_string(index=False))

# ── Query 2: Quarter over quarter change using window function ─────
q2 = """
SELECT
    YEAR_QUARTER,
    COUNT(*) AS filings,
    COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY YEAR_QUARTER) AS qoq_change
FROM fund_filings
GROUP BY YEAR_QUARTER
ORDER BY YEAR_QUARTER
"""

print("\n── Query 2: QoQ change with window function ──────────────")
print(pd.read_sql_query(q2, conn).to_string(index=False))

# ── Query 3: Duplicate detection ──────────────────────────────────
q3 = """
SELECT
    ENTITYNAME,
    COUNT(*) AS total_filings,
    MIN(FILING_DATE) AS first_filing,
    MAX(FILING_DATE) AS last_filing
FROM fund_filings
WHERE ENTITYNAME IS NOT NULL
GROUP BY ENTITYNAME
HAVING COUNT(*) > 5
ORDER BY total_filings DESC
LIMIT 15
"""

print("\n── Query 3: Funds with most filings (possible series) ────")
print(pd.read_sql_query(q3, conn).to_string(index=False))

# ── Query 4: Data completeness check ──────────────────────────────
q4 = """
SELECT
    COUNT(*)                                                AS total_records,
    SUM(CASE WHEN ENTITYNAME IS NULL THEN 1 ELSE 0 END)    AS missing_name,
    SUM(CASE WHEN FILING_DATE IS NULL THEN 1 ELSE 0 END)   AS missing_date,
    SUM(CASE WHEN TOTALOFFERINGAMOUNT IS NULL
             OR TOTALOFFERINGAMOUNT = 0 THEN 1 ELSE 0 END) AS missing_amount,
    ROUND(100.0 * SUM(CASE WHEN TOTALOFFERINGAMOUNT > 0
                           THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_with_amount
FROM fund_filings
"""

print("\n── Query 4: Data completeness audit ──────────────────────")
print(pd.read_sql_query(q4, conn).to_string(index=False))

conn.close()
print("\nDatabase saved to data/processed/funds.db")