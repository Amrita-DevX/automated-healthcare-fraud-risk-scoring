"""
train_isolation_forest.py

This script trains the Isolation Forest fraud detection model
using engineered feature data and logs the trained model to MLflow.

IMPORTANT:
- This script is run during MODEL TRAINING (not daily inference)
- It produces a versioned ML model artifact
"""

import yaml
import pandas as pd
import mlflow
import mlflow.sklearn
from pathlib import Path

# Import the pipeline definition (preprocessing + model)
from pipelines.fraud_pipeline import build_fraud_pipeline


# --------------------------------------------------
# Load configuration
# --------------------------------------------------
CONFIG_PATH = Path("config/config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

MODEL_CONFIG = config["model"]
PATH_CONFIG = config["paths"]
MLFLOW_CONFIG = config["mlflow"]


# --------------------------------------------------
# Load feature data
# --------------------------------------------------
# This data is assumed to be already engineered
# (from SQL + Python feature assembly)
feature_path = Path(PATH_CONFIG["feature_table"])

print(f"Loading feature data from {feature_path}")
features_df = pd.read_parquet(feature_path)

# --------------------------------------------------
# Separate features from identifiers
# --------------------------------------------------
# We never train on IDs
ID_COLUMNS = ["provider_id"]  # adjust later if needed
X = features_df.drop(columns=ID_COLUMNS, errors="ignore")

print(f"Training data shape: {X.shape}")


# --------------------------------------------------
# Initialize MLflow experiment
# --------------------------------------------------
mlflow.set_experiment(MLFLOW_CONFIG["experiment_name"])

with mlflow.start_run():

    # --------------------------------------------------
    # Build fraud detection pipeline
    # --------------------------------------------------
    pipeline = build_fraud_pipeline(
        contamination=MODEL_CONFIG["contamination"],
        random_state=MODEL_CONFIG["random_state"]
    )

    # --------------------------------------------------
    # Train model
    # --------------------------------------------------
    print("Training Isolation Forest model...")
    pipeline.fit(X)

    # --------------------------------------------------
    # Log parameters to MLflow
    # --------------------------------------------------
    mlflow.log_param("model_type", "IsolationForest")
    mlflow.log_param("contamination", MODEL_CONFIG["contamination"])
    mlflow.log_param("random_state", MODEL_CONFIG["random_state"])
    mlflow.log_param("num_features", X.shape[1])

    # --------------------------------------------------
    # Log trained model artifact
    # --------------------------------------------------
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="fraud_model"
    )

    print("Model training completed and logged to MLflow.")
