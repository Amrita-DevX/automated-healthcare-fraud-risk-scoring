-- ============================================
-- Provider-level fraud features
-- ============================================

SELECT
    provider_id,

    COUNT(*) AS total_claims,
    COUNT(DISTINCT desynpuf_id) AS unique_beneficiaries,

    AVG(clm_pmt_amt) AS avg_claim_amount,
    SUM(clm_pmt_amt) AS total_billed_amount,

    -- Red flags
    CASE
        WHEN COUNT(*) > 500 THEN 1 ELSE 0
    END AS high_volume_provider_flag,

    CASE
        WHEN AVG(clm_pmt_amt) > 15000 THEN 1 ELSE 0
    END AS high_avg_cost_provider_flag

FROM claims
GROUP BY provider_id;