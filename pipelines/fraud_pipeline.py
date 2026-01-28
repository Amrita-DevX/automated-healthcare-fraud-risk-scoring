"""
fraud_pipeline.py

This module defines the machine learning pipeline used for
healthcare fraud risk scoring.

IMPORTANT:
- This file DOES NOT load data
- This file DOES NOT train the model
- This file DOES NOT save or score data

Its ONLY responsibility is to define:
    feature preprocessing + Isolation Forest model
in a single reusable sklearn Pipeline.
"""

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def build_fraud_pipeline(
    contamination: float,
    random_state: int
) -> Pipeline: 
    """
    Build and return an sklearn Pipeline for fraud detection.

    Parameters
    ----------
    contamination : float
        Expected proportion of anomalies in the data.
        In fraud detection, this is usually low (e.g. 1–5%).

    random_state : int
        Ensures reproducibility of Isolation Forest results.

    Returns
    -------
    Pipeline
        A fitted-unfitted sklearn Pipeline consisting of:
        - Missing value imputation
        - Feature standardization
        - Isolation Forest model
    """

    # --------------------------------------------------
    # Step 1: Handle missing values
    # --------------------------------------------------
    # Why?
    # - SQL aggregates may produce NULLs
    # - Isolation Forest cannot handle NaNs
    #
    # Why median?
    # - Robust to extreme outliers
    # - Standard choice for fraud-related numeric features
    imputer = SimpleImputer(
        strategy="median"
    )

    # --------------------------------------------------
    # Step 2: Standardize features
    # --------------------------------------------------
    # Why?
    # - Fraud features have very different scales
    #   (e.g., total_claims vs avg_claim_amount)
    # - Scaling prevents large-magnitude features
    #   from dominating the model
    scaler = StandardScaler()

    # --------------------------------------------------
    # Step 3: Isolation Forest model
    # --------------------------------------------------
    # Why Isolation Forest?
    # - Designed for anomaly detection
    # - Scales well to large datasets
    # - Widely used in fraud detection
    model = IsolationForest(
        n_estimators=200,        # number of trees
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1                # use all CPU cores
    )

    # --------------------------------------------------
    # Combine all steps into ONE pipeline
    # --------------------------------------------------
    # This ensures:
    # - Same preprocessing during training and inference
    # - No data leakage
    # - Reproducibility
    pipeline = Pipeline(
        steps=[
            ("imputer", imputer),
            ("scaler", scaler),
            ("model", model)
        ]
    )

    return pipeline
