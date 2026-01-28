"""
batch_score_claims.py

Batch inference script for healthcare fraud risk scoring.

This script:
- Loads the registered Isolation Forest model from MLflow (via alias)
- Scores providers using engineered features
- Assigns risk bands
- Writes outputs for downstream investigation teams

This script is designed to be scheduled (e.g., via Tidal).
"""

import pandas as pd
import mlflow
import mlflow.sklearn
from pathlib import Path


def assign_risk_band(score: float) -> str:
    """
    Convert anomaly score into a human-readable risk band.

    Higher score = higher fraud risk.
    """
    if score >= 0.95:
        return "HIGH"
    elif score >= 0.85:
        return "MEDIUM"
    else:
        return "LOW"


def batch_score_providers(
    feature_path: str,
    model_name: str,
    model_alias: str,
    output_dir: str
) -> None:
    """
    Run batch fraud risk scoring for providers.

    Parameters
    ----------
    feature_path : str
        Path to ML-ready feature table.
    model_name : str
        Registered MLflow model name.
    model_alias : str
        MLflow model alias (e.g., staging, production).
    output_dir : str
        Directory to write scoring outputs.
    """

    print("Loading feature table...")
    df = pd.read_parquet(feature_path)

    provider_ids = df["provider_id"]
    X = df.drop(columns=["provider_id"])

    # --------------------------------------------------
    # Load registered model from MLflow using alias
    # --------------------------------------------------
    print(f"Loading model '{model_name}' with alias '{model_alias}'")
    model_uri = f"models:/{model_name}@{model_alias}"
    model = mlflow.sklearn.load_model(model_uri)

    # --------------------------------------------------
    # Generate anomaly scores
    # --------------------------------------------------
    # Isolation Forest: higher score = more anomalous
    scores = -model.score_samples(X)

    # --------------------------------------------------
    # Build output table
    # --------------------------------------------------
    results_df = pd.DataFrame({
        "provider_id": provider_ids,
        "fraud_risk_score": scores
    })

    # Normalize scores for readability (0–1 scale)
    score_min = results_df["fraud_risk_score"].min()
    score_max = results_df["fraud_risk_score"].max()

    if score_max > score_min:
        results_df["fraud_risk_score"] = (
            (results_df["fraud_risk_score"] - score_min) /
            (score_max - score_min)
        )
    else:
        results_df["fraud_risk_score"] = 0.0

    # Assign risk bands
    results_df["risk_band"] = results_df["fraud_risk_score"].apply(assign_risk_band)

    # --------------------------------------------------
    # Persist outputs (latest + dated snapshot)
    # --------------------------------------------------
    from datetime import date

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    today_str = date.today().isoformat()

    # Latest files (overwrite each run)
    latest_parquet = output_dir / "provider_fraud_scores.parquet"
    latest_csv = output_dir / "provider_fraud_scores.csv"

    # Dated snapshot files (append history)
    dated_parquet = output_dir / f"provider_fraud_scores_{today_str}.parquet"
    dated_csv = output_dir / f"provider_fraud_scores_{today_str}.csv"

    # Write outputs
    results_df.to_parquet(latest_parquet, index=False)
    results_df.to_csv(latest_csv, index=False)

    results_df.to_parquet(dated_parquet, index=False)
    results_df.to_csv(dated_csv, index=False)

    print("Fraud scoring completed.")
    print("Outputs written to:")
    print(f" - Latest: {latest_parquet}")
    print(f" - Latest: {latest_csv}")
    print(f" - Snapshot: {dated_parquet}")
    print(f" - Snapshot: {dated_csv}")


if __name__ == "__main__":

    FEATURE_PATH = "data/processed/fraud_features.parquet"
    MODEL_NAME = "fraud_model"
    MODEL_ALIAS = "staging"   # MLflow alias
    OUTPUT_DIR = "data/outputs"

    batch_score_providers(
        feature_path=FEATURE_PATH,
        model_name=MODEL_NAME,
        model_alias=MODEL_ALIAS,
        output_dir=OUTPUT_DIR
    )
