"""
provider_features.py

This module is responsible for generating provider-level
behavioral features used for fraud detection.

Key points:
- Features are aggregated at the PROVIDER level
- SQL performs aggregation logic
- Python performs orchestration and cleanup
- No model training happens here
"""

import sqlite3
import pandas as pd
from pathlib import Path


def load_provider_features(db_path: str) -> pd.DataFrame:
    """
    Load provider-level fraud features from the database.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    pd.DataFrame
        Provider-level feature table where:
        - One row = one provider
        - Columns = behavioral fraud features
    """

    # --------------------------------------------------
    # Establish database connection
    # --------------------------------------------------
    # We keep DB access inside this function to:
    # - avoid global state
    # - make testing easier
    conn = sqlite3.connect(db_path)

    # --------------------------------------------------
    # Load SQL logic
    # --------------------------------------------------
    # Provider features depend on claim-derived signals,
    # which are already handled inside provider_features.sql
    sql_path = Path("sql/provider_features.sql")

    with open(sql_path, "r") as f:
        provider_sql = f.read()

    # --------------------------------------------------
    # Execute SQL and load into pandas
    # --------------------------------------------------
    provider_df = pd.read_sql(provider_sql, conn)

    # --------------------------------------------------
    # Close DB connection
    # --------------------------------------------------
    conn.close()

    # --------------------------------------------------
    # Basic sanity cleanup
    # --------------------------------------------------
    # Ensure numeric columns are truly numeric
    # (SQLite can sometimes return strings)
    for col in provider_df.columns:
        if col != "provider_id":
            provider_df[col] = pd.to_numeric(
                provider_df[col],
                errors="coerce"
            )

    # --------------------------------------------------
    # Replace missing values
    # --------------------------------------------------
    # Missing values can occur for:
    # - providers with very few claims
    # - edge aggregation cases
    #
    # We do NOT impute here aggressively;
    # final imputation happens in the ML pipeline.
    provider_df = provider_df.fillna(0)

    return provider_df
