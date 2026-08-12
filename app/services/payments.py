from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import User
from app.models.payments import Plan, Subscription


async def ensure_default_plans(session: AsyncSession) -> None:
    defaults = [
        ("free", "Free", 0, 20),
        ("pro", "Pro", 1900, None),
    ]
    for code, name, price, limit in defaults:
        plan = await session.scalar(select(Plan).where(Plan.code == code))
        if not plan:
            session.add(
                Plan(
                    code=code,
                    name=name,
                    monthly_price_cents=price,
                    prediction_limit=limit,
                )
            )
    await session.commit()


async def create_demo_checkout(session: AsyncSession, user: User, plan_code: str) -> tuple[Subscription, str]:
    plan = await session.scalar(select(Plan).where(Plan.code == plan_code))
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    reference = f"demo_{uuid4().hex}"
    subscription = Subscription(
        user_id=user.id,
        plan_id=plan.id,
        status="active",
        provider="demo",
        provider_reference=reference,
        current_period_end=datetime.now(UTC) + timedelta(days=30),
    )
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription, attribute_names=["plan"])
    return subscription, f"https://payments.example.test/checkout/{reference}"

