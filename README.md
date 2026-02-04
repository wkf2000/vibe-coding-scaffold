# vibe-coding-scaffold
GenAI Service Template (uv + FastAPI + Streamlit + Supabase + NVIDIA NIM)
A reusable, interview-friendly skeleton for building production-minded GenAI services fast.

## Stack
- Backend: FastAPI (Python 3.11+)
- Frontend: Streamlit
- DB: Supabase (Postgres) via `supabase-py`
- LLM: NVIDIA NIM via HTTP API key
- Tooling: `uv` + `ruff` + `mypy` + `pytest`
- Deploy: Docker + docker-compose 

## Quickstart (Docker)
```bash
cp .env.example .env
docker compose up --build
```
Backend docs: http://localhost:8000/docs  
Frontend: http://localhost:8501

## Quickstart (Dev, no Docker)
Backend:
```bash
cd backend
uv sync --extra dev
uv run uvicorn app.main:app --reload --port 8000
```
Frontend:
```bash
cd frontend
uv sync --extra dev
uv run streamlit run streamlit_app.py --server.port 8501
```

