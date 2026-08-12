from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.matches import Match
from app.models.predictions import Prediction
from app.schemas.predictions import PredictionRead
from app.services.auth import get_current_user
from app.services.predictions import create_prediction

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/matches/{match_id}", response_model=PredictionRead, dependencies=[Depends(get_current_user)])
async def predict_match(match_id: int, session: AsyncSession = Depends(get_session)):
    match = await session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return await create_prediction(session, match)


@router.get("/matches/{match_id}", response_model=list[PredictionRead])
async def list_match_predictions(match_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Prediction).where(Prediction.match_id == match_id).order_by(Prediction.created_at.desc())
    )
    return list(result.scalars())

