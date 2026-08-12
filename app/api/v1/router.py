from fastapi import APIRouter

from app.api.v1 import auth, events, matches, payments, predictions, ws

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(matches.router)
api_router.include_router(predictions.router)
api_router.include_router(payments.router)
api_router.include_router(events.router)
api_router.include_router(ws.router)

