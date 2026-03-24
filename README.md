# 🏎️ f1-ai-lab

A portfolio of three AI/ML projects built around Formula 1 racing data.
Each project demonstrates a distinct layer of the modern AI engineering stack.

## Projects

| # | Project | Stack | Status |
|---|---------|-------|--------|
| 1 | [F1 Race Predictor](./project1_race_predictor/) | pandas · XGBoost · FastAPI | 🚧 In Progress |
| 2 | [F1 Race Analyst Agent](./project2_race_analyst/) | LangChain · ChromaDB · Ollama | 📋 Planned |
| 3 | [F1 Strategy Co-pilot](./project3_strategy_copilot/) | LangGraph · React · FastAPI | 📋 Planned |

## Setup

Each project has its own `requirements.txt` and `README.md`.
Navigate into any project folder and follow its setup guide.
```bash
# Example: run Project 1
cd project1_race_predictor
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Architecture

This is a monorepo. Shared tooling (CI, linting) lives at the root.
Project-specific code, data, and notebooks are self-contained within each project folder.