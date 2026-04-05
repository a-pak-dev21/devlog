# PriceObserver

PriceObserver is an end-to-end project that collects crypto pair prices from multiple exchanges, stores snapshot-based market data in PostgreSQL, and exposes it via a REST API (FastAPI).

**Focus:** backend/data workflow — collection → validation → storage → queries → API → Docker/Compose → testing.

---

## What’s implemented

### Data collection (API clients)
- Exchange clients (e.g., Binance, Coinbase) via HTTP requests.
- Normalized output format:
  - `base`, `quote`, `pair`
  - `stock_exchange`
  - `price`
- Collect prices for multiple pairs within a single snapshot run.

### PostgreSQL + SQLAlchemy Core
- Database schema (SQLAlchemy Core):
  - `pairs`
  - `exchanges`
  - `snapshots`
  - `prices`
  - `errors`
- Persistence logic:
  - create `snapshot`
  - upsert for `pairs` / `exchanges`
  - batch insert into `prices`
  - error logging/persisting into `errors`
- Constraints & indexing (unique combinations, indexes on key fields).

### Query layer (DB queries)
- Select/join/filter utilities:
  - latest snapshot
  - pair timeseries
  - snapshot spreads
  - list pairs / exchanges
  - error listing

### FastAPI (REST API)
- Core endpoints:
  - `GET /health`
  - `GET /ready` (DB connectivity check)
  - `GET /pairs`
  - `GET /pairs/history` (timeseries)
  - `GET /exchanges`
  - `GET /last-snapshot`
  - `GET /spreads/{snapshot_id}`
  - `POST /post-snapshot` (run a snapshot + persist to DB)
- Pydantic schemas for request/response models.

### Docker / Docker Compose
- Dockerfile for the app.
- Docker Compose setup:
  - FastAPI app
  - PostgreSQL db
  - healthchecks + depends_on
  - persistent volumes
- Configurable via environment variables / settings.

### Testing
- Basic API testing via `TestClient`:
  - smoke tests
  - validation cases (400)
  - empty responses
  - POST snapshot flow

---

## Tech stack

- Python 3.12
- FastAPI + Pydantic v2
- PostgreSQL
- SQLAlchemy Core + psycopg
- Docker + Docker Compose
- Pytest / FastAPI TestClient
- Logging (structured configuration)

---

## Project structure (example)

- `app/`
  - `api/` — FastAPI endpoints + schemas
  - `clients/` — exchange clients
  - `db/` — models, persistence, queries
  - `services/` — orchestration (run_snapshot → save_snapshot)
  - `analysis/` — analytics utilities (optional)
  - `settings.py` — configuration
  - `logging_config.py` — logging setup

---

## Run locally (without Docker)

1) Create venv and install dependencies:
```bash
pip install -r requirements.txt

	2.	Ensure PostgreSQL is reachable and env variables are configured (DATABASE_URL or POSTGRES_*).
	3.	Start the API:

uvicorn app.api.fast_api:app --reload --host 0.0.0.0 --port 8000


⸻

Run with Docker Compose
	1.	Build and start services:

docker compose up --build

	2.	Open Swagger UI:

	•	http://localhost:8000/docs

⸻

Main endpoints
	•	GET /health — API liveness check
	•	GET /ready — DB connectivity check
	•	GET /pairs — list available pairs
	•	GET /pairs/history?base=BTC&quote=USDT&start=...&end=...&exchange=...
	•	GET /exchanges — list exchanges
	•	GET /last-snapshot — latest snapshot
	•	GET /spreads/{snapshot_id} — spreads for all pairs within a snapshot
	•	POST /post-snapshot — run a snapshot and persist results
Example body:

{
  "pairs": [["BTC","USDT"], ["ETH","USDT"]]
}


⸻

Roadmap (next steps)
	•	Env/config: remove remaining hardcoding, dev/test/prod modes
	•	Routers: structure API with APIRouter, API versioning
	•	Async stack: async HTTP collection (httpx) + (optional) async DB
	•	Alembic: database migrations
	•	Background jobs: Redis + Celery/RQ for scheduled snapshots
	•	CI/CD: GitHub Actions (lint/test/build)
	•	Deploy: AWS (EC2/Lightsail) + production compose setup

⸻

Notes

The project is developed iteratively: first correctness and structure, then production practices (migrations, CI/CD, async, deployment). Data is stored in PostgreSQL and served through a REST API.

