# Inventory Service

A small FastAPI service for reserving stock safely. It demonstrates request validation, domain errors, idempotent reservation keys, health checks, tests, containers, and CI.

## Run locally

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
pytest
```

Open `http://127.0.0.1:8000/docs` for the interactive API.
