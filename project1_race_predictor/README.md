![CI](https://github.com/YOUR_GITHUB_USERNAME/f1-ai-lab/actions/workflows/ci.yml/badge.svg)

# Project 1 - F1 Race Predictor

Predicts F1 race finishing positions using historical data from the
Jolpica-F1 API (open source Ergast replacement).

## Stack

| Layer | Tool |
|-------|------|
| Data fetching | Jolpica-F1 API · requests |
| Data processing | pandas · numpy |
| ML | XGBoost · LightGBM · scikit-learn |
| Experiment tracking | MLflow |
| Serving | FastAPI · Streamlit |
| Testing | pytest · pytest-cov |
| CI | GitHub Actions |

## Sprint Progress

- [x] Sprint 1 - Repo setup, CI pipeline, data fetcher, EDA
- [ ] Sprint 2 - Feature engineering, model training, cross-validation
- [ ] Sprint 3 - MLflow tracking, FastAPI endpoint, Streamlit dashboard

## Project Structure
```
project1_race_predictor/
├── data/
│   ├── raw/            # API responses, never edited by hand
│   └── processed/      # cleaned DataFrames, plots, feature tables
├── notebooks/
│   └── 01_eda.ipynb    # Sprint 1 exploratory data analysis
├── src/
│   └── data_fetcher.py # Jolpica-F1 API client
├── tests/
│   └── test_data_fetcher.py
└── requirements.txt
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data Source

[Jolpica-F1](https://github.com/jolpica/jolpica-f1) - free, open source,
no API key required. A community-maintained Ergast-compatible API covering
every F1 season from 1950 to present.

> The original Ergast API was shut down in early 2025. Jolpica is the
> recommended replacement with identical endpoints and JSON schema.

## Key EDA Findings (Sprint 1)

| Finding | Modelling Implication |
|---|---|
| Grid position strongly correlates with finish | Primary feature in Sprint 2 |
| Constructor explains significant result variance | Encode as categorical feature |
| DNF rate ~15–20% across seasons | Handle as separate result class |
| Points system is non-linear (P1=25, P2=18) | Use finish position as target, not points |

## Sample Output
```
   driver_name  position  constructor
0  Max Verstappen       1    red_bull
1   Sergio Perez       2    red_bull
2  Fernando Alonso      3  aston_martin
```