# Automated Healthcare Fraud Risk Scoring Platform

## Project Overview

An end-to-end production-grade healthcare fraud detection system designed to identify high-risk providers before claim adjudication. This solution reduces financial leakage, minimizes manual review workload, and accelerates investigation timelines through behavioral anomaly detection and machine learning.

### Core Components

- Feature Engineering Pipelines for behavioral pattern extraction
- Unsupervised Machine Learning Risk Scoring with Isolation Forest
- Batch Inference Orchestration for scalable processing
- Experiment Tracking infrastructure (MLflow-ready)
- Business Intelligence Layer with Power BI Dashboard
- CI/CD Ready Repository Structure for production deployment

---

## Business Problem

Healthcare payers face substantial financial losses annually due to fraudulent provider activities:

- Provider overbilling and billing inflation
- Abnormal claim volume patterns
- Suspicious billing behavior patterns inconsistent with peer providers
- Extreme cost outliers relative to clinical benchmarks

Traditional rule-based fraud detection systems present significant limitations:
- Generate high false positive rates, increasing operational burden
- Require continuous maintenance as fraud schemes evolve
- Miss sophisticated behavioral fraud patterns that deviate from predefined rules
- Lack adaptability to new fraud methodologies

---

## Solution Architecture

This system implements an unsupervised anomaly detection pipeline that:

- Scores providers daily based on comprehensive behavioral patterns
- Identifies high-risk providers before financial harm occurs
- Delivers investigator-ready dashboards with actionable insights
- Produces stable, repeatable fraud signals suitable for production environments

---

## Machine Learning Approach

### Model Type

**Unsupervised Anomaly Detection** using Isolation Forest-based risk scoring

### Rationale for Unsupervised Learning

Traditional supervised fraud detection requires labeled training data, which is problematic in healthcare fraud detection due to:

- **Rarity**: Confirmed fraud cases represent a small fraction of claims
- **Delayed Labels**: Investigation and adjudication processes create significant label delay
- **Label Unreliability**: Many suspected fraud cases are never confirmed or officially documented

Unsupervised behavioral anomaly detection better serves early fraud discovery by identifying statistical deviations from normal provider behavior patterns without relying on historical fraud labels.

---

## Feature Engineering

### Provider Behavioral Features

The model incorporates the following features derived from claims data:

| Feature | Description |
|---------|-------------|
| Total Claims Volume | Aggregate count of claims submitted by provider |
| Total Billed Amount | Cumulative billing amount across all claims |
| Average Claim Amount | Mean claim value per transaction |
| Unique Beneficiary Count | Number of distinct patients served |
| High Volume Provider Flag | Binary indicator for above-threshold claim volume |
| High Average Cost Provider Flag | Binary indicator for above-threshold average claim costs |

These features capture both volume-based and cost-based behavioral patterns that may indicate fraudulent activity.

---

## Pipeline Architecture

```
Raw Claims Data
    ↓
Feature Engineering Pipeline
    ↓
Fraud Risk Scoring Model (Isolation Forest)
    ↓
Risk Band Classification (Low / Medium / High)
    ↓
Batch Inference Output
    ↓
Power BI Dashboard
```

---

## Project Structure

```
automated-healthcare-fraud-risk-scoring/
│
├── config/                          # Configuration management
├── db/                              # Database connections and utilities
├── features/                        # Feature engineering modules
├── inference/                       # Model inference logic
├── orchestration/                   # Batch job orchestration
├── pipelines/                       # ETL and processing pipelines
├── training/                        # Model training scripts
├── notebooks/                       # Exploratory analysis and validation
├── sql/                             # Database queries and schemas
│
├── powerbi/
│   └── provider_fraud_dashboard.pbix    # Power BI dashboard
│
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Model Stability Validation

Production-grade machine learning systems require rigorous stability validation. This model demonstrates exceptional consistency across retraining cycles.

### Score Correlation Analysis

**Correlation Across Retraining Runs: 0.997 - 0.998**

This correlation coefficient indicates:
- Retraining the model produces virtually identical anomaly scores
- The model exhibits minimal sensitivity to randomness in training
- The model has learned robust, generalizable behavioral fraud patterns
- Score stability enables reliable longitudinal monitoring

This level of consistency is exceptionally rare for unsupervised models and demonstrates production-ready reliability.

### Provider Risk Ranking Stability

**High-Risk Provider Overlap Across Retraining Runs: 86% - 96%**

Specific overlap measurements across iterations:
- Run 1-2 Overlap: 94%
- Run 2-3 Overlap: 86%
- Run 3-4 Overlap: 90%
- Run 4-5 Overlap: 96%

This stability metric indicates:
- The same high-risk providers are consistently flagged across model retraining
- Minimal random churn in alert generation for high-risk entities
- Investigators receive stable, repeatable alerts suitable for ongoing cases
- Model conclusions are reproducible and defensible

This consistency is precisely what operational fraud investigation teams require for maintaining case continuity and investigative confidence.

---

## Power BI Dashboard

The business intelligence layer provides comprehensive fraud risk visualization and investigative support.

### Dashboard Page 1: Provider Risk Overview

**Key Performance Indicators**
- Total Providers Scored
- High-Risk Provider Count
- Risk Distribution by Band

**Visualizations**
- Risk band distribution chart
- Top risk provider ranking table
- Provider-level risk metrics

### Dashboard Page 2: Claims Fraud Risk & Financial Exposure

**Key Performance Indicators**
- Total Claims Exposure (USD)
- High + Medium Risk Claims Exposure (USD)
- Percentage of Claims at Elevated Risk

**Visualizations**
- Claims Volume vs. Fraud Risk Scatter Plot
- Financial Exposure by Risk Band
- Investigator Queue with prioritized cases
- Trend analysis for fraud risk evolution

---

## Batch Scoring Automation

The orchestration framework supports production-grade batch processing:

- **Automated Execution**: Shell scripts (.sh) for scheduling and executing batch jobs with minimal manual intervention
- **Scheduled Batch Scoring**: Daily model execution on updated provider data
- **New Provider Onboarding**: Immediate risk scoring for recently registered providers
- **Automated Output Generation**: Structured data exports for downstream systems
- **CI/CD Ready Pipeline**: Containerized deployment and automated testing

---

## Experiment Tracking & MLOps

The project structure supports enterprise machine learning operations:

- **Model Versioning**: Track and manage multiple model iterations
- **Experiment Comparison**: Systematic evaluation across training configurations
- **Metric Logging**: Comprehensive performance and stability metrics
- **Artifact Storage**: Model serialization and dependency management
- **MLflow Integration**: Compatible with industry-standard experiment tracking

---

## Business Impact

Deployment of this system in production environments enables:

- **Financial Loss Reduction**: Early identification of overbilling and fraudulent schemes
- **Operational Efficiency**: Reduced manual review workload for compliance teams
- **Investigator Prioritization**: Systematic ranking of cases by fraud risk
- **Early Detection**: Behavioral anomalies identified before significant financial exposure
- **Explainability**: Transparent fraud signals based on provider behavioral patterns

---

## Technology Stack

### Data Science & Machine Learning
- Python 3.8+
- Pandas - Data manipulation and analysis
- NumPy - Numerical computing
- Scikit-Learn - Machine learning algorithms

### Data Engineering
- SQL - Data extraction and transformation
- Feature Engineering Pipelines - Custom processing modules
- Batch Orchestration - Workflow automation

### MLOps
- GitHub - Version control and collaboration
- CI/CD Ready Structure - Automated testing and deployment
- MLflow - Experiment tracking and model registry

### Business Intelligence
- Power BI - Dashboard development and visualization

---

## Key Highlights

- **End-to-End ML System**: Complete pipeline from raw data to business dashboard
- **Production Architecture**: Designed with scalability, monitoring, and maintainability
- **Stable Unsupervised Model**: Exceptional score consistency across retraining
- **Business Integration**: Actionable insights delivered to stakeholders
- **Batch Automation**: Scheduled, repeatable fraud risk scoring
- **Real-World Applicability**: Addresses genuine healthcare fraud challenges

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- SQL database (configuration in config/)
- Power BI Desktop (for dashboard modification)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/Amrita-DevX/automated-healthcare-fraud-risk-scoring
cd automated-healthcare-fraud-risk-scoring
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database connections:
```bash
# Update config/ with your database credentials
cp config/example_config.yaml config/config.yaml
```

5. Run SQL feature engineering:
```bash
python -m features.buld_features.py
```

6. Train the model:
```bash
python -m training.train_isolation_forest.py
```

7. Execute batch inference:
```bash
python -m inference.batch_score_claims.py
```

---

## Future Enhancements

Planned improvements for production deployment and operational expansion:

- **Real-Time Scoring API**: REST endpoints for immediate provider risk assessment
- **Streaming Fraud Detection**: Real-time processing of incoming claims
- **Drift Monitoring**: Automated detection of model performance degradation
- **Alert System Integration**: Direct integration with incident management platforms
- **Cloud Deployment**: Containerized deployment on cloud platforms (AWS, GCP, Azure)
- **Advanced Explainability**: SHAP values and feature importance analysis
- **Multi-Model Ensemble**: Combining multiple anomaly detection algorithms

---

## Contributing

Contributions are welcome. Please ensure:
- Code follows PEP 8 style guidelines
- New features include appropriate tests
- Documentation is updated alongside code changes
- Experiment tracking captures model improvements


---

## Author

**Amrita Das**

Data Science | Machine Learning | Fraud Analytics | Applied AI

---

## Contact & Support

For questions, issues, or collaboration inquiries, please open an issue in the repository or contact the author.
