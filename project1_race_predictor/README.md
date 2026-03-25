# F1 Race Predictor

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
[Jolpica-F1 API](https://github.com/jolpica/jolpica-f1) — free, open source,
no API key required. Ergast-compatible endpoints covering every F1 season
from 1950 to present. Maintained by the F1 open source community.