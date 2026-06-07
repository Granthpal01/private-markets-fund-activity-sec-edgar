import pandas as pd
import os

# ── Step 1: Load the three key files for Q1 2023 ──────────────────
offering = pd.read_csv("data/raw/2023q1/2023Q1_d/OFFERING.tsv",
                       sep="\t", low_memory=False)

issuers = pd.read_csv("data/raw/2023q1/2023Q1_d/ISSUERS.tsv",
                      sep="\t", low_memory=False)

submission = pd.read_csv("data/raw/2023q1/2023Q1_d/FORMDSUBMISSION.tsv",
                         sep="\t", low_memory=False)

# ── Step 2: Filter to investment funds only ────────────────────────
funds = offering[offering["INDUSTRYGROUPTYPE"] == "Pooled Investment Fund"]

# ── Step 3: Keep one issuer row per filing ─────────────────────────
primary_issuers = issuers[issuers["IS_PRIMARYISSUER_FLAG"] == "YES"]

# ── Step 4: Join funds + issuer names ─────────────────────────────
merged = funds.merge(
    primary_issuers[["ACCESSIONNUMBER", "ENTITYNAME",
                     "CITY", "STATEORCOUNTRY", "ENTITYTYPE"]],
    on="ACCESSIONNUMBER",
    how="left"
)

# ── Step 5: Join filing date and submission type ───────────────────
final = merged.merge(
    submission[["ACCESSIONNUMBER", "FILING_DATE", "SUBMISSIONTYPE"]],
    on="ACCESSIONNUMBER",
    how="left"
)

# ── Step 6: Clean dates, extract year and quarter ─────────────────
final["FILING_DATE"] = pd.to_datetime(final["FILING_DATE"],
                                       format="%d-%b-%Y")
final["YEAR"]         = final["FILING_DATE"].dt.year
final["QUARTER"]      = final["FILING_DATE"].dt.quarter
final["YEAR_QUARTER"] = (final["YEAR"].astype(str)
                         + " Q" + final["QUARTER"].astype(str))

# ── Step 7: Save ───────────────────────────────────────────────────
os.makedirs("data/processed", exist_ok=True)
final.to_csv("data/processed/2023q1_clean.csv", index=False)

# ── Step 8: Summary ───────────────────────────────────────────────
print(f"Total investment fund filings : {len(final):,}")
print(f"Unique fund names             : {final['ENTITYNAME'].nunique():,}")
print(f"\nStrategy breakdown:")
print(final["INVESTMENTFUNDTYPE"].value_counts())
print(f"\nSubmission types:")
print(final["SUBMISSIONTYPE"].value_counts())