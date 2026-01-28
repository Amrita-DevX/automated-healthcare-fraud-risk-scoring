-- ============================================
-- Beneficiary-level fraud features
-- ============================================

SELECT
    desynpuf_id,

    COUNT(*) AS total_claims,
    COUNT(DISTINCT provider_id) AS unique_providers,

    SUM(clm_pmt_amt) AS total_spend,
    AVG(clm_pmt_amt) AS avg_claim_amount,

    -- Utilization flags
    CASE
        WHEN COUNT(*) > 50 THEN 1 ELSE 0
    END AS high_utilization_flag,

    CASE
        WHEN COUNT(DISTINCT provider_id) > 10 THEN 1 ELSE 0
    END AS provider_shopping_flag

FROM claims
GROUP BY desynpuf_id;
