#!/bin/bash 
set -e

echo "Starting daily healthcare fraud risk batch job..."

# Step 1: Build ML-ready features
python -m features.build_features

# Step 2: Run batch fraud scoring
python -m inference.batch_score_claims

echo "Daily batch job completed successfully."
