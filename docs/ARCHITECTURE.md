# Architecture

The platform is a FastAPI service backed by PostgreSQL, Redis, SQLAlchemy, and Alembic. The code is organized around domain services rather than route-only logic so ingestion, prediction, authentication, billing, and event publishing can be tested independently.

## Core Flow

1. A sports data provider returns a normalized snapshot of competitions, teams, and fixtures.
2. The ingestion service upserts that snapshot into SQL tables.
3. In the same database transaction, ingestion writes `outbox_events` rows for match changes.
4. A worker reads pending outbox rows, publishes them to Redis, and marks them published.
5. WebSocket clients subscribe to `/api/v1/ws/events` and receive Redis-published domain events.
6. Authenticated users can request predictions for matches. Prediction creation also writes an outbox event.

## Modules

- `app/api`: FastAPI routes and WebSocket endpoint.
- `app/models`: SQLAlchemy ORM models.
- `app/schemas`: Pydantic request and response contracts.
- `app/services`: business logic for auth, ingestion, predictions, payments, and events.
- `alembic`: database migration history.
- `scripts`: operational entry points for seeding and outbox publishing.

## Prediction Model

`demo-elo-v1` is intentionally deterministic and transparent. It estimates team strength from stored team identifiers, applies a home advantage, derives expected goals, and normalizes home/draw/away probabilities with softmax. It is designed as a replaceable model boundary rather than a final betting model.

## Eventing

The transactional outbox prevents losing domain events when a database write succeeds but Redis publish fails. Producers only write database rows. The worker is responsible for delivery and retry tracking.

