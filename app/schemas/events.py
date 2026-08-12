from datetime import datetime

from pydantic import BaseModel


class EventRead(BaseModel):
    id: int
    event_type: str
    aggregate_type: str
    aggregate_id: str
    payload: dict
    status: str
    created_at: datetime
    published_at: datetime | None

    model_config = {"from_attributes": True}

