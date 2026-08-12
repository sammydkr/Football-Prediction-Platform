from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.events import OutboxEvent
from app.schemas.events import EventRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)])


@router.get("/outbox", response_model=list[EventRead])
async def list_outbox(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(OutboxEvent).order_by(OutboxEvent.id.desc()).limit(50))
    return list(result.scalars())

