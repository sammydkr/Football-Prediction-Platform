from datetime import datetime

from pydantic import BaseModel


class PlanRead(BaseModel):
    id: int
    code: str
    name: str
    monthly_price_cents: int
    prediction_limit: int | None

    model_config = {"from_attributes": True}


class CheckoutRequest(BaseModel):
    plan_code: str


class CheckoutSession(BaseModel):
    provider: str
    checkout_url: str
    reference: str


class SubscriptionRead(BaseModel):
    id: int
    status: str
    provider: str
    provider_reference: str
    current_period_end: datetime
    plan: PlanRead

    model_config = {"from_attributes": True}

