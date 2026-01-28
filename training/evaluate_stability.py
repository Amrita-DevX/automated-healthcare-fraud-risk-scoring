"""
evaluate_stability.py

Evaluates the stability of the Isolation Forest fraud model
by comparing anomaly scores across multiple training runs.

This is critical for unsupervised models where accuracy
metrics are unavailable.
"""

import numpy as np
import pandas as pd
from pathlib import Path

from pipelines.fraud_pipeline import build_fraud_pipeline


def evaluate_model_stability(
    feature_path: str,
    contamination: float,
    base_random_state: int,
    n_runs: int = 5,
    top_n: int = 50
) -> None:
    """
    Evaluate stability of anomaly detection across multiple runs.

    Parameters
    ----------
    feature_path : str
        Path to ML-ready feature table (parquet).
    contamination : float
        Expected fraud rate.
    base_random_state : int
        Base random seed.
    n_runs : int
        Number of retraining runs.
    top_n : int
        Number of top anomalies to compare.
    """

    print("Loading feature data...")
    df = pd.read_parquet(feature_path)

    ids = df["provider_id"]
    X = df.drop(columns=["provider_id"])

    all_scores = []

    print(f"Running {n_runs} stability iterations...")

    for i in range(n_runs):
        seed = base_random_state + i

        pipeline = build_fraud_pipeline(
            contamination=contamination,
            random_state=seed
        )

        pipeline.fit(X)

        # Isolation Forest: higher = more anomalous
        scores = -pipeline.score_samples(X)

        run_df = pd.DataFrame({
            "provider_id": ids,
            "score": scores,
            "run": i
        })

        all_scores.append(run_df)

    scores_df = pd.concat(all_scores)

    # --------------------------------------------------
    # 1. Score correlation check
    # --------------------------------------------------
    print("\nStability Check 1: Score Correlation")

    pivot_scores = scores_df.pivot(
        index="provider_id",
        columns="run",
        values="score"
    )

    corr_matrix = pivot_scores.corr()
    print(corr_matrix)

    # --------------------------------------------------
    # 2. Top-N overlap check
    # --------------------------------------------------
    print(f"\nStability Check 2: Top-{top_n} Overlap")

    top_sets = []
    for run in range(n_runs):
        top_providers = (
            scores_df[scores_df["run"] == run]
            .sort_values("score", ascending=False)
            .head(top_n)["provider_id"]
            .tolist()
        )
        top_sets.append(set(top_providers))

    overlaps = []
    for i in range(len(top_sets) - 1):
        overlap = len(top_sets[i].intersection(top_sets[i + 1])) / top_n
        overlaps.append(overlap)

    print(f"Top-{top_n} overlap ratios between consecutive runs:")
    for i, ov in enumerate(overlaps):
        print(f"Run {i} vs Run {i+1}: {ov:.2f}")

    # --------------------------------------------------
    # 3. Interpretation hint
    # --------------------------------------------------
    print("\nInterpretation Guide:")
    print("- Correlation > 0.85 indicates strong stability")
    print("- Top-N overlap > 70% is considered acceptable")
    print("- Large deviations indicate unreliable anomaly behavior")


if __name__ == "__main__":

    FEATURE_PATH = "data/processed/fraud_features.parquet"

    evaluate_model_stability(
        feature_path=FEATURE_PATH,
        contamination=0.02,
        base_random_state=42,
        n_runs=5,
        top_n=50
    )
