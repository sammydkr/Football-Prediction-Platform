from datetime import datetime

from pydantic import BaseModel


class PredictionRead(BaseModel):
    id: int
    match_id: int
    model_version: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    expected_home_goals: float
    expected_away_goals: float
    created_at: datetime

    model_config = {"from_attributes": True}

