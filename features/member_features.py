"""
member_features.py

This module is responsible for generating member-level
behavioral features used for fraud detection.

Key points:
- Features are aggregated at the MEMBER (beneficiary) level
- SQL performs aggregation logic
- Python performs orchestration and cleanup
- No model training happens here
"""

import sqlite3
import pandas as pd
from pathlib import Path


def load_member_features(db_path: str) -> pd.DataFrame:
    """
    Load member-level fraud features from the database.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    pd.DataFrame
        Member-level feature table where:
        - One row = one member
        - Columns = behavioral fraud features
    """

    # --------------------------------------------------
    # Establish database connection
    # --------------------------------------------------
    # DB access is kept local to the function
    # to avoid global state and improve testability
    conn = sqlite3.connect(db_path)

    # --------------------------------------------------
    # Load SQL logic
    # --------------------------------------------------
    # Member features depend on claim-derived signals,
    # which are already handled inside member_features.sql
    sql_path = Path("sql/member_features.sql")

    with open(sql_path, "r") as f:
        member_sql = f.read()

    # --------------------------------------------------
    # Execute SQL and load into pandas
    # --------------------------------------------------
    member_df = pd.read_sql(member_sql, conn)

    # --------------------------------------------------
    # Close DB connection
    # --------------------------------------------------
    conn.close()

    # --------------------------------------------------
    # Basic sanity cleanup
    # --------------------------------------------------
    # SQLite may return numeric columns as strings,
    # so we explicitly coerce types
    for col in member_df.columns:
        if col != "desynpuf_id":
            member_df[col] = pd.to_numeric(
                member_df[col],
                errors="coerce"
            )

    # --------------------------------------------------
    # Replace missing values
    # --------------------------------------------------
    # Missing values usually occur for:
    # - members with very few claims
    # - edge aggregation cases
    #
    # Final imputation will happen in the ML pipeline
    member_df = member_df.fillna(0)

    return member_df
