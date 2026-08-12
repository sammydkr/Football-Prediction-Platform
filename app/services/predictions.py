from math import exp

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.matches import Match
from app.models.predictions import Prediction
from app.services.events import add_outbox_event

MODEL_VERSION = "demo-elo-v1"


def _team_strength(team_id: int) -> float:
    return 1.0 + (team_id % 7) / 10


def _softmax(values: list[float]) -> list[float]:
    exps = [exp(value) for value in values]
    total = sum(exps)
    return [value / total for value in exps]


async def create_prediction(session: AsyncSession, match: Match) -> Prediction:
    home_strength = _team_strength(match.home_team_id) + 0.18
    away_strength = _team_strength(match.away_team_id)
    expected_home = round(1.15 * home_strength, 2)
    expected_away = round(1.05 * away_strength, 2)
    home, draw, away = _softmax([expected_home - expected_away, 0.22, expected_away - expected_home])
    prediction = Prediction(
        match_id=match.id,
        model_version=MODEL_VERSION,
        home_win_probability=round(home, 4),
        draw_probability=round(draw, 4),
        away_win_probability=round(away, 4),
        expected_home_goals=expected_home,
        expected_away_goals=expected_away,
    )
    session.add(prediction)
    await session.flush()
    await add_outbox_event(
        session,
        event_type="prediction.created",
        aggregate_type="prediction",
        aggregate_id=prediction.id,
        payload={"match_id": match.id, "model_version": MODEL_VERSION},
    )
    await session.commit()
    await session.refresh(prediction)
    return prediction

