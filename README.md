# 🏎️ f1-ai-lab

> *From raw lap data to real-time race strategy — an open source AI Engineering portfolio powered by F1.*

Building intelligent F1 systems with ML, RAG agents, and multi-agent AI — end-to-end open source portfolio.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Source-100%25-brightgreen?style=flat-square)

---

## 📌 About

**f1-ai-lab** is a monorepo of three AI Engineering projects built around Formula 1 data. It covers the full spectrum of modern AI Engineering — from classical ML pipelines and RAG-powered chatbots to multimodal multi-agent systems — all built using open source tools and delivered in agile sprints.

This portfolio is designed to demonstrate practical, production-ready AI Engineering skills to recruiters and hiring managers.

---

## 🗂️ Repository Structure

```
f1-ai-lab/
│
├── project-1-race-predictor/       # ML · Data Engineering
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   │   ├── ingestion/              # Ergast API data fetcher
│   │   ├── features/               # Feature engineering pipeline
│   │   ├── models/                 # XGBoost / LightGBM training
│   │   └── api/                    # FastAPI prediction endpoint
│   ├── tests/
│   ├── Dockerfile
│   └── README.md
│
├── project-2-analyst-agent/        # NLP · RAG · Agents
│   ├── data/
│   ├── src/
│   │   ├── scraper/                # Race report scraper
│   │   ├── embeddings/             # sentence-transformers pipeline
│   │   ├── retrieval/              # ChromaDB vector store
│   │   └── agent/                  # LangChain RAG agent
│   ├── tests/
│   ├── Dockerfile
│   └── README.md
│
└── project-3-strategy-copilot/     # GenAI · Vision · Full-stack
    ├── frontend/                   # React app
    ├── backend/                    # FastAPI server
    ├── agents/                     # LangGraph multi-agent system
    ├── vision/                     # Fine-tuned vision model
    ├── tests/
    ├── docker-compose.yml
    └── README.md
```

---

## 🚀 Projects

### Project 1 — F1 Race Predictor
> Predict driver finishing positions using historical F1 race data.

**What it does:** Ingests historical race data from the Ergast API, engineers features (grid position, pit stop strategy, weather, tyre compound), trains an XGBoost/LightGBM model, and serves predictions through a FastAPI endpoint with a Streamlit dashboard.

| Layer | Tools |
|-------|-------|
| Data | pandas, FastF1, Ergast API |
| ML | scikit-learn, XGBoost, LightGBM |
| Tracking | MLflow |
| Serving | FastAPI, Streamlit |
| Infra | Docker, GitHub Actions |

**Sprints:** Data pipeline → Model training → API + Dashboard

---

### Project 2 — F1 Race Analyst Agent
> Ask questions about F1 history and get answers grounded in real race documents.

**What it does:** Scrapes F1 race reports and Wikipedia pages, embeds them with sentence-transformers, stores them in ChromaDB, and builds a RAG pipeline with LangChain backed by a local LLM running via Ollama. Includes a live standings tool and is evaluated with RAGAS.

| Layer | Tools |
|-------|-------|
| Embeddings | sentence-transformers |
| Vector DB | ChromaDB / FAISS |
| LLM | Ollama (Mistral / LLaMA 3) |
| Orchestration | LangChain |
| UI | Gradio |
| Evaluation | RAGAS |
| Infra | Docker, HuggingFace Spaces |

**Sprints:** Knowledge base → RAG agent → Evaluation + Deployment

---

### Project 3 — F1 Strategy Co-pilot
> A multimodal multi-agent system for real-time race strategy analysis.

**What it does:** Fine-tunes a vision model on telemetry chart images, orchestrates a multi-agent system (Analyst → Strategist → Reporter) using LangGraph, and delivers recommendations through a React + FastAPI full-stack app with real-time WebSocket updates and full LLM observability.

| Layer | Tools |
|-------|-------|
| Agents | LangGraph, LangChain |
| Vision | LLaVA / Idefics (fine-tuned) |
| Observability | LangSmith, Arize Phoenix |
| Full-stack | React, FastAPI, WebSockets |
| Infra | Docker, HuggingFace Spaces |

**Sprints:** Vision model → Multi-agent system → Full-stack app + Deployment

---

## 🛠️ Open Source Stack

All tools used in this portfolio are 100% free and open source — no paid APIs, no proprietary services.

```
Data          pandas · polars · FastF1 · Ergast API
ML            scikit-learn · XGBoost · LightGBM · MLflow
LLM / Agents  Ollama · LangChain · LangGraph · sentence-transformers
Vector DB     ChromaDB · FAISS
Serving       FastAPI · Streamlit · Gradio
Infra         Docker · GitHub Actions · HuggingFace Spaces
Evaluation    RAGAS · pytest
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.11+
- Docker
- Git

### Clone the repo
```bash
git clone https://github.com/<your-username>/f1-ai-lab.git
cd f1-ai-lab
```

### Set up a project
Each project has its own environment. Navigate into the project folder and follow its `README.md`.

```bash
# Example: Project 1
cd project-1-race-predictor
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📅 Agile Methodology

This portfolio is built sprint-by-sprint to maximise learning, commit frequency, and project quality.

| Sprint | Focus |
|--------|-------|
| Sprint 1 | Data foundation & repo setup |
| Sprint 2 | Core model or agent pipeline |
| Sprint 3 | Serving, UI, evaluation & deployment |

### Commit convention
```
feat:      new feature
fix:       bug fix
docs:      documentation update
test:      adding or updating tests
refactor:  code cleanup
chore:     tooling or config changes
```

---

## 📊 Skills Demonstrated

| Skill | P1 | P2 | P3 |
|-------|----|----|----|
| Data pipelines | ✅ | | |
| ML model training | ✅ | | |
| Experiment tracking | ✅ | | |
| REST API development | ✅ | | ✅ |
| Embeddings & vector DBs | | ✅ | |
| RAG pipelines | | ✅ | |
| LLM integration | | ✅ | ✅ |
| AI Agents | | ✅ | ✅ |
| Multi-agent orchestration | | | ✅ |
| Vision / multimodal AI | | | ✅ |
| Fine-tuning | | | ✅ |
| Observability & evaluation | | ✅ | ✅ |
| Full-stack development | | | ✅ |
| Docker & deployment | ✅ | ✅ | ✅ |

---

## 📄 License

MIT License — free to use, learn from, and build upon.

---

<p align="center">Built with ❤️ and open source tools · Guided by agile methodology</p>
