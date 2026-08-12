from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.payments import ensure_default_plans


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with SessionLocal() as session:
        await ensure_default_plans(session)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Football prediction API with match ingestion, auth, billing, outbox events, and WebSockets.",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": settings.app_name}


app.include_router(api_router)

