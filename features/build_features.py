"""
build_features.py

This script assembles all feature components into a single
ML-ready feature table.

Responsibilities:
- Load provider-level features
- Load member-level features
- Merge feature sets
- Write final feature table to disk

IMPORTANT:
- This script does NOT train models
- This script does NOT define ML pipelines
- This script produces the feature contract for training
"""

import pandas as pd
from pathlib import Path

from features.provider_features import load_provider_features
from features.member_features import load_member_features


def build_feature_table(db_path: str, output_path: str) -> None:
    """
    Build and persist the final ML feature table.

    Parameters
    ----------
    db_path : str
        Path to SQLite database.
    output_path : str
        Path where the ML feature table will be written.
    """

    print("Starting feature assembly...")

    # --------------------------------------------------
    # Load provider-level features
    # --------------------------------------------------
    print("Loading provider features...")
    provider_df = load_provider_features(db_path)

    # --------------------------------------------------
    # Load member-level features
    # --------------------------------------------------
    print("Loading member features...")
    member_df = load_member_features(db_path)

    # --------------------------------------------------
    # Merge features
    # --------------------------------------------------
    # IMPORTANT DESIGN DECISION:
    # - Provider is the primary ML entity
    # - Member features are aggregated independently
    #
    # For v1 of this project:
    # - We keep provider features as the core training unit
    # - Member features are NOT joined yet
    #
    # Reason:
    # - Provider fraud is the dominant signal
    # - Avoids complex joins that dilute explanation
    #
    # Member features remain available for future extension
    feature_df = provider_df.copy()

    # --------------------------------------------------
    # Final sanity checks
    # --------------------------------------------------
    print("Performing final sanity checks...")

    # Drop any duplicate rows (defensive)
    feature_df = feature_df.drop_duplicates(subset="provider_id")

    # Ensure all columns except ID are numeric
    for col in feature_df.columns:
        if col != "provider_id":
            feature_df[col] = pd.to_numeric(
                feature_df[col],
                errors="coerce"
            )

    # Replace remaining missing values with 0
    feature_df = feature_df.fillna(0)

    # --------------------------------------------------
    # Persist feature table
    # --------------------------------------------------
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    feature_df.to_parquet(output_path, index=False)

    print(f"Feature table written to {output_path}")
    print(f"Final feature shape: {feature_df.shape}")


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":

    DB_PATH = "data/fraud_claims.db"
    OUTPUT_PATH = "data/processed/fraud_features.parquet"

    build_feature_table(DB_PATH, OUTPUT_PATH)
