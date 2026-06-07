# PriceObserver

PriceObserver is a backend/data engineering project for collecting cryptocurrency price data from multiple exchange APIs, storing snapshot-based market data in PostgreSQL, and exposing the collected data through a FastAPI REST API.

The project focuses on a practical backend workflow:

```text
external APIs → validation → snapshot creation → PostgreSQL storage → queries → REST API → Docker Compose → API testing
```

---

## Overview

PriceObserver collects crypto pair prices from supported exchanges such as Binance and Coinbase.

Each collection run is stored as a separate snapshot, which makes it possible to query the latest market data, inspect historical prices, compare prices across exchanges, and track collection errors.

The project is designed as a portfolio-level backend service that demonstrates:

- external API integration;
- PostgreSQL schema design;
- SQLAlchemy Core data layer;
- Alembic migrations;
- FastAPI endpoints;
- JWT-protected admin actions;
- Docker Compose local environment;
- API workflow testing with Postman;
- basic automated tests.

---

## Features

### Data Collection

- Collects prices from external exchange APIs.
- Supports multiple trading pairs per snapshot run.
- Normalizes exchange-specific API responses into a unified internal format.
- Stores successful price results and collection errors separately.

### Snapshot-Based Storage

Each data collection run creates a snapshot.

A snapshot may contain:

- prices from multiple exchanges;
- multiple trading pairs;
- successful records;
- failed collection attempts saved as errors.

This makes the project more realistic than a simple “latest price only” script.

### PostgreSQL Persistence

The database stores:

- trading pairs;
- exchanges;
- snapshots;
- prices;
- collection errors.

The persistence layer includes:

- pair/exchange upserts;
- snapshot creation;
- batch price inserts;
- error persistence;
- constraints and indexes on key fields.

### FastAPI REST API

The API exposes endpoints for:

- API health checks;
- database readiness checks;
- listing pairs and exchanges;
- creating new snapshots;
- reading the latest snapshot;
- querying pair history;
- calculating spreads between exchanges.

### Authentication

Snapshot creation is protected with JWT-based admin authentication.

The authentication flow:

```text
POST /auth/login → receive JWT access token → use Bearer token for protected endpoints
```

### Docker Compose

The project can be started locally with Docker Compose.

The Compose setup includes:

- FastAPI application container;
- PostgreSQL database container;
- persistent database volume;
- service health checks;
- environment-based configuration.

### Postman Collection

The repository includes a Postman collection for testing the main API workflow:

- health checks;
- admin login;
- JWT token handling;
- authenticated snapshot creation;
- read endpoints;
- negative authentication cases.

---

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic v2
- PostgreSQL
- SQLAlchemy Core
- Alembic
- psycopg
- Docker
- Docker Compose
- Pytest / FastAPI TestClient
- Postman
- JWT authentication
- Python logging

---

## High-Level Architecture

```text
External Exchange APIs
        ↓
Exchange Clients
        ↓
Snapshot Service
        ↓
Repository Layer / SQLAlchemy Core
        ↓
PostgreSQL
        ↓
FastAPI REST API
        ↓
Postman / Swagger / Tests
```

---

## Project Structure

```text
price-observer/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   ├── deps/
│   │   └── schemas/
│   ├── clients/
│   ├── db/
│   │   ├── models/
│   │   ├── queries/
│   │   └── repositories/
│   ├── services/
│   ├── settings.py
│   └── logging_config.py
├── alembic/
├── tests/
├── postman/
│   ├── price_observer_collection.json
│   └── price_observer_local_environment.example.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

> The exact internal structure may change as the project evolves, but the main separation is: API layer, service layer, database layer, exchange clients, tests, and infrastructure files.

---

## Environment Variables

Create a local `.env` file from the provided example:

```bash
cp .env.example .env
```

Then fill in the required values.

Example variables:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=price_observer

JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your_admin_password_hash
```

Do not commit real secrets, passwords, JWT keys, or access tokens.

---

## Run with Docker Compose

Build and start the services:

```bash
docker compose up --build
```

After startup, the API should be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

Health check:

```text
GET http://localhost:8000/health
```

Database readiness check:

```text
GET http://localhost:8000/ready
```

---

## Database Migrations

The project uses Alembic for database migrations.

Apply migrations:

```bash
alembic upgrade head
```

If running inside Docker:

```bash
docker compose exec api alembic upgrade head
```

Create a new migration after schema changes:

```bash
alembic revision --autogenerate -m "migration message"
```

Then apply it:

```bash
alembic upgrade head
```

---

## API Authentication

The protected snapshot creation endpoint requires a JWT Bearer token.

### 1. Login

```http
POST /auth/login
```

The login endpoint uses OAuth2 password form data.

Request body type:

```text
application/x-www-form-urlencoded
```

Fields:

```text
username=<admin_username>
password=<admin_password>
```

Successful response:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

### 2. Use the token

For protected requests, send the token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

---

## Main API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/health` | API liveness check | No |
| GET | `/ready` | Database connectivity check | No |
| POST | `/auth/login` | Admin login and JWT token creation | No |
| POST | `/post-snapshot` | Run a new price snapshot and persist results | Yes |
| GET | `/pairs` | List available trading pairs | No |
| GET | `/pairs/history` | Get historical prices for a pair | No |
| GET | `/exchanges` | List available exchanges | No |
| GET | `/last-snapshot` | Get the latest saved snapshot | No |
| GET | `/spreads/{snapshot_id}` | Get spreads between exchanges for a snapshot | No |

---

## Create a Snapshot

Endpoint:

```http
POST /post-snapshot
```

Headers:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Example request body:

```json
{
  "pairs": [
    ["BTC", "USDT"],
    ["ETH", "USDT"]
  ]
}
```

Example response:

```json
{
  "snapshot_id": 1,
  "rows_inserted": 4
}
```

The exact number of inserted rows depends on the number of pairs, supported exchanges, and successful external API responses.

---

## Query Pair History

Endpoint:

```http
GET /pairs/history
```

Example:

```text
/pairs/history?base=BTC&quote=USDT&exchange=binance
```

Optional filters may include:

- `base`
- `quote`
- `exchange`
- `start`
- `end`

---

## Get Snapshot Spreads

Endpoint:

```http
GET /spreads/{snapshot_id}
```

Example:

```text
/spreads/1
```

This endpoint returns price differences between exchanges for pairs collected within the same snapshot.

---

## API Testing with Postman

This project includes a Postman collection for testing the main API workflow.

Files:

```text
postman/price_observer_collection.json
postman/price_observer_local_environment.example.json
```

The collection covers:

- API health check;
- database readiness check;
- admin login;
- JWT token saving into the Postman environment;
- authenticated snapshot creation;
- reading exchanges, pairs, latest snapshot, history, and spreads;
- negative authentication cases:
  - missing token;
  - invalid token;
  - invalid credentials.

### How to use

1. Import both files into Postman.
2. Select the imported environment.
3. Fill in:
   - `base_url`
   - `username`
   - `password`
4. Run the `Login` request.
5. The access token will be saved automatically.
6. Run the workflow requests.

---

## Tests

The project contains basic automated API tests.

The current test suite covers:

- health check;
- database readiness;
- request validation cases;
- empty response cases;
- snapshot creation flow;
- authentication behavior.

Run tests locally:

```bash
pytest
```

Run tests inside Docker:

```bash
docker compose exec api pytest
```

> Note: the test setup is still being improved. The next development step is to make the test workflow more explicit and prepare it for CI/CD.

---

## Development Workflow

Typical local development flow:

```bash
docker compose up --build
```

Apply migrations if needed:

```bash
docker compose exec api alembic upgrade head
```

Run tests:

```bash
docker compose exec api pytest
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

Use the Postman collection for the full API workflow.

---

## Current Project Status

Implemented:

- exchange API clients;
- normalized price collection;
- snapshot-based persistence;
- PostgreSQL schema;
- SQLAlchemy Core data layer;
- Alembic migrations;
- FastAPI REST API;
- JWT-based admin authentication;
- Docker Compose setup;
- Postman collection;
- basic automated API tests.

In progress / planned:

- improve test structure and pytest knowledge;
- add GitHub Actions CI workflow;
- add optional Redis/background jobs for scheduled snapshots;
- improve deployment setup;
- add production-oriented logging/monitoring improvements.

---

## Roadmap

### Short-Term

- Improve README and project documentation.
- Finalize `.env.example`.
- Review and clean GitHub repository.
- Improve pytest test structure.
- Add GitHub Actions for automated test runs.

### Mid-Term

- Add Redis for caching or background job coordination.
- Add scheduled snapshot collection.
- Add background worker using Celery, RQ, or another suitable tool.
- Add deployment documentation.

### Long-Term

- Deploy the API.
- Add monitoring/logging improvements.
- Add a lightweight dashboard or analytics layer.
- Extend support for more exchanges.
- Add more advanced historical analytics.

---

## Notes

PriceObserver is developed iteratively.

The first goal is correctness and a clear backend/data workflow.

The next goal is improving project maturity through tests, CI/CD, background jobs, and deployment.