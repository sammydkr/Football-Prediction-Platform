# Football Prediction Platform

FastAPI football prediction platform with PostgreSQL, Redis, SQLAlchemy, Alembic, Pydantic, JWT auth with refresh-token rotation, demo sports-data ingestion, a versioned prediction service, transactional outbox events, WebSockets, demo subscriptions, Docker, tests, and CI.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Open:

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Event stream: `ws://localhost:8000/api/v1/ws/events`

## Main Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/matches/ingest-demo`
- `GET /api/v1/matches`
- `POST /api/v1/predictions/matches/{match_id}`
- `GET /api/v1/billing/plans`
- `POST /api/v1/billing/checkout`
- `GET /api/v1/events/outbox`

## Local Development

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install -e ".[dev]"
alembic upgrade head
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

Run checks:

```bash
ruff check .
pytest
```

## Demo Auth Flow

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo@example.com\",\"password\":\"correct horse battery\"}"

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo@example.com\",\"password\":\"correct horse battery\"}"
```

Use the returned access token as `Authorization: Bearer <token>` for protected demo ingestion, prediction creation, billing checkout, and outbox inspection.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Security](docs/SECURITY.md)

