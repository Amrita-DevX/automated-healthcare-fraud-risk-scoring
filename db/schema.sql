-- =====================================================
-- Database Schema for Automated Fraud Claims Scoring
-- SQLite version 
-- =====================================================

-- -----------------------------
-- Beneficiaries (Members)
-- Source: Beneficiary_2008/2009/2010.csv
-- -----------------------------
CREATE TABLE IF NOT EXISTS beneficiaries (
    desynpuf_id TEXT PRIMARY KEY,        -- Unique beneficiary ID
    dob TEXT,                             -- Date of birth
    gender INTEGER,                      -- 1 = Male, 2 = Female
    race INTEGER,                        -- CMS race code
    state TEXT,                          -- State code
    county TEXT,                         -- County code

    chronic_diabetes INTEGER,
    chronic_chf INTEGER,
    chronic_ckd INTEGER,
    chronic_copd INTEGER,
    chronic_cancer INTEGER
);

-- -----------------------------
-- Claims (Inpatient + Outpatient)
-- Source: Inpatient_Claims.csv, Outpatient_Claims.csv
-- -----------------------------
CREATE TABLE IF NOT EXISTS claims (
    clm_id TEXT PRIMARY KEY,              -- Claim ID
    desynpuf_id TEXT,                     -- Beneficiary ID
    provider_id TEXT,                     -- Provider number
    claim_type TEXT,                     -- INPATIENT / OUTPATIENT

    clm_from_dt TEXT,                     -- Claim start date
    clm_thru_dt TEXT,                     -- Claim end date
    clm_pmt_amt REAL,                     -- Claim payment amount

    principal_diagnosis TEXT,
    procedure_code TEXT,

    FOREIGN KEY (desynpuf_id)
        REFERENCES beneficiaries(desynpuf_id)
);
