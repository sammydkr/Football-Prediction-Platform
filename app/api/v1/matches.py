from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.session import get_session
from app.models.matches import Match
from app.schemas.matches import MatchRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=list[MatchRead])
async def list_matches(
    status: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(Match)
        .options(joinedload(Match.competition), joinedload(Match.home_team), joinedload(Match.away_team))
        .order_by(Match.kickoff_at)
    )
    if status:
        query = query.where(Match.status == status)
    result = await session.execute(query)
    return list(result.scalars())


@router.get("/{match_id}", response_model=MatchRead)
async def get_match(match_id: int, session: AsyncSession = Depends(get_session)):
    match = await session.scalar(
        select(Match)
        .where(Match.id == match_id)
        .options(joinedload(Match.competition), joinedload(Match.home_team), joinedload(Match.away_team))
    )
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/ingest-demo", dependencies=[Depends(get_current_user)])
async def ingest_demo(session: AsyncSession = Depends(get_session)):
    from app.core.config import settings
    from app.services.demo_provider import DemoSportsDataProvider
    from app.services.ingestion import ingest_snapshot

    provider = DemoSportsDataProvider(settings.demo_provider_seed)
    return await ingest_snapshot(session, await provider.fetch_snapshot())

