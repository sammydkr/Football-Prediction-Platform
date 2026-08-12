from datetime import datetime

from pydantic import BaseModel


class CompetitionRead(BaseModel):
    id: int
    name: str
    country: str

    model_config = {"from_attributes": True}


class TeamRead(BaseModel):
    id: int
    name: str
    short_name: str

    model_config = {"from_attributes": True}


class MatchRead(BaseModel):
    id: int
    provider_id: str
    competition: CompetitionRead
    home_team: TeamRead
    away_team: TeamRead
    kickoff_at: datetime
    status: str
    home_score: int | None
    away_score: int | None

    model_config = {"from_attributes": True}

