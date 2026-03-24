# Project 1 - F1 Race Predictor

Predicts F1 race finishing positions using historical data from the Ergast API.

## Stack
- **Data:** Ergast API, pandas
- **ML:** XGBoost, LightGBM, scikit-learn
- **Tracking:** MLflow
- **Serving:** FastAPI + Streamlit

## Sprint Progress
- [x] Sprint 1: Repo setup, data pipeline, EDA
- [ ] Sprint 2: Feature engineering, model training
- [ ] Sprint 3: MLflow, API endpoint, dashboard

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data Source
[Ergast Motor Racing API](http://ergast.com/mrd/) — free, no API key required.
Covers every F1 season from 1950 to present.