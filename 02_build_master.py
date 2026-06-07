import pandas as pd
import os

# ── All 12 quarters we downloaded ─────────────────────────────────
QUARTERS = [
    "2023q1", "2023q2", "2023q3", "2023q4",
    "2024q1", "2024q2", "2024q3", "2024q4",
    "2025q1", "2025q2", "2025q3", "2025q4",
]

def process_quarter(quarter):
    """Load, filter, join and clean one quarter of Form D data."""
    
    base = f"data/raw/{quarter}"
    
    # Find the subfolder — it's named like 2023Q1_d
    subfolder = [f for f in os.listdir(base) if os.path.isdir(f"{base}/{f}")][0]
    path = f"{base}/{subfolder}"
    
    # Load three files
    offering   = pd.read_csv(f"{path}/OFFERING.tsv",
                              sep="\t", low_memory=False)
    issuers    = pd.read_csv(f"{path}/ISSUERS.tsv",
                              sep="\t", low_memory=False)
    submission = pd.read_csv(f"{path}/FORMDSUBMISSION.tsv",
                              sep="\t", low_memory=False)

    # Filter to investment funds
    funds = offering[offering["INDUSTRYGROUPTYPE"] == "Pooled Investment Fund"]

    # Keep primary issuer only
    primary = issuers[issuers["IS_PRIMARYISSUER_FLAG"] == "YES"]

    # Join funds + issuers
    merged = funds.merge(
        primary[["ACCESSIONNUMBER", "ENTITYNAME",
                 "CITY", "STATEORCOUNTRY", "ENTITYTYPE"]],
        on="ACCESSIONNUMBER",
        how="left"
    )

    # Join filing date
    merged = merged.merge(
        submission[["ACCESSIONNUMBER", "FILING_DATE", "SUBMISSIONTYPE"]],
        on="ACCESSIONNUMBER",
        how="left"
    )

    # Parse dates
    merged["FILING_DATE"]  = pd.to_datetime(merged["FILING_DATE"],
                                             format="%d-%b-%Y")
    merged["YEAR"]         = merged["FILING_DATE"].dt.year
    merged["QUARTER"]      = merged["FILING_DATE"].dt.quarter
    merged["YEAR_QUARTER"] = (merged["YEAR"].astype(str)
                               + " Q" + merged["QUARTER"].astype(str))
    merged["SOURCE"]       = quarter

    return merged


# ── Loop through all quarters ──────────────────────────────────────
all_quarters = []

for q in QUARTERS:
    df = process_quarter(q)
    print(f"{q} : {len(df):,} filings")
    all_quarters.append(df)

# ── Stack into one master dataset ─────────────────────────────────
master = pd.concat(all_quarters, ignore_index=True)

# ── Save ───────────────────────────────────────────────────────────
os.makedirs("data/processed", exist_ok=True)
master.to_csv("data/processed/master_funds.csv", index=False)

print(f"\nTotal filings across all quarters : {len(master):,}")
print(f"Unique fund names                 : {master['ENTITYNAME'].nunique():,}")
print(f"\nStrategy breakdown:")
print(master["INVESTMENTFUNDTYPE"].value_counts())