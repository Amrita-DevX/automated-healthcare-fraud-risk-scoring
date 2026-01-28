-- ============================================
-- Claim-level fraud features
-- ============================================

SELECT
    clm_id,
    desynpuf_id,
    provider_id,
    claim_type,

    clm_pmt_amt,
    JULIANDAY(clm_thru_dt) - JULIANDAY(clm_from_dt) AS length_of_stay,

    -- Cost flags
    CASE 
        WHEN clm_pmt_amt > 20000 THEN 1 ELSE 0 
    END AS high_cost_flag,

    CASE
        WHEN (JULIANDAY(clm_thru_dt) - JULIANDAY(clm_from_dt)) <= 1 
             AND clm_pmt_amt > 10000
        THEN 1 ELSE 0
    END AS short_stay_high_cost_flag

FROM claims;
