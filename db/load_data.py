"""
Load CMS DE-SynPUF synthetic data into SQLite database

This script:
1. Creates a SQLite connection
2. Loads Beneficiary CSVs (2008–2010)
3. Loads Inpatient and Outpatient claims
4. Writes data into normalized tables

Run this ONCE after downloading CSVs.
"""
import sqlite3
import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Paths
# -----------------------------------------------------
DB_PATH = Path("data/fraud_claims.db")
RAW_DATA_PATH = Path("data/raw")

BENEFICIARY_FILES = [
    RAW_DATA_PATH / "Beneficiary_2008.csv",
    RAW_DATA_PATH / "Beneficiary_2009.csv",
    RAW_DATA_PATH / "Beneficiary_2010.csv",
]

INPATIENT_FILE = RAW_DATA_PATH / "Inpatient_Claims.csv"
OUTPATIENT_FILE = RAW_DATA_PATH / "Outpatient_Claims.csv"

# -----------------------------------------------------
# Connect to SQLite
# -----------------------------------------------------
conn = sqlite3.connect(DB_PATH)

# =====================================================
# Load BENEFICIARIES
# =====================================================
print("Loading beneficiaries...")

beneficiary_dfs = []

for file in BENEFICIARY_FILES:
    df = pd.read_csv(file)
    beneficiary_dfs.append(df)

beneficiaries = pd.concat(beneficiary_dfs, ignore_index=True)

# ---- CMS column mapping (based on your samples) ----
BENEFICIARY_COLUMN_MAP = {
    "DESYNPUF_ID": "desynpuf_id",
    "BENE_BIRTH_DT": "dob",
    "BENE_SEX_IDENT_CD": "gender",
    "BENE_RACE_CD": "race",
    "SP_STATE_CODE": "state",
    "BENE_COUNTY_CD": "county",
    "SP_DIABETES": "chronic_diabetes",
    "SP_CHF": "chronic_chf",
    "SP_COPD": "chronic_copd",
    "SP_CNCR": "chronic_cancer",
}

# Keep only columns that exist in the CSV
available_cols = [c for c in BENEFICIARY_COLUMN_MAP if c in beneficiaries.columns]
beneficiaries = beneficiaries[available_cols]

# Rename columns to standardized names
beneficiaries = beneficiaries.rename(columns=BENEFICIARY_COLUMN_MAP)

# Ensure all chronic condition columns exist
for col in [
    "chronic_diabetes",
    "chronic_chf",
    "chronic_ckd",
    "chronic_copd",
    "chronic_cancer",
]:
    if col not in beneficiaries.columns:
        beneficiaries[col] = 0

# Remove duplicate beneficiaries across years
beneficiaries = beneficiaries.drop_duplicates(subset="desynpuf_id")

# Write to database
beneficiaries.to_sql(
    "beneficiaries",
    conn,
    if_exists="append",
    index=False
)

print(f"Loaded {len(beneficiaries)} unique beneficiaries")

# =====================================================
# Load CLAIMS (Inpatient + Outpatient)
# =====================================================
print("Loading claims...")

def load_claims(file_path: Path, claim_type: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Columns verified from your sample CSVs
    df = df[
        [
            "CLM_ID",
            "DESYNPUF_ID",
            "PRVDR_NUM",
            "CLM_FROM_DT",
            "CLM_THRU_DT",
            "CLM_PMT_AMT",
            "ICD9_DGNS_CD_1",
            "ICD9_PRCDR_CD_1",
        ]
    ]

    df = df.rename(columns={
        "CLM_ID": "clm_id",
        "DESYNPUF_ID": "desynpuf_id",
        "PRVDR_NUM": "provider_id",
        "CLM_FROM_DT": "clm_from_dt",
        "CLM_THRU_DT": "clm_thru_dt",
        "CLM_PMT_AMT": "clm_pmt_amt",
        "ICD9_DGNS_CD_1": "principal_diagnosis",
        "ICD9_PRCDR_CD_1": "procedure_code",
    })

    df["claim_type"] = claim_type
    return df


inpatient_claims = load_claims(INPATIENT_FILE, "INPATIENT")
outpatient_claims = load_claims(OUTPATIENT_FILE, "OUTPATIENT")

claims = pd.concat([inpatient_claims, outpatient_claims], ignore_index=True)

# Drop duplicate claims just in case
claims = claims.drop_duplicates(subset="clm_id")

# Write to database
claims.to_sql(
    "claims",
    conn,
    if_exists="append",
    index=False
)

print(f"Loaded {len(claims)} total claims")

# -----------------------------------------------------
# Close DB connection
# -----------------------------------------------------
conn.close()
print("Data loading completed successfully.")