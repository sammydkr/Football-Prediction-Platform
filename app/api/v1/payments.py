from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models.auth import User
from app.models.payments import Plan, Subscription
from app.schemas.payments import CheckoutRequest, CheckoutSession, PlanRead, SubscriptionRead
from app.services.auth import get_current_user
from app.services.payments import create_demo_checkout, ensure_default_plans

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/plans", response_model=list[PlanRead])
async def list_plans(session: AsyncSession = Depends(get_session)):
    await ensure_default_plans(session)
    result = await session.execute(select(Plan).order_by(Plan.monthly_price_cents))
    return list(result.scalars())


@router.post("/checkout", response_model=CheckoutSession)
async def checkout(
    payload: CheckoutRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    subscription, checkout_url = await create_demo_checkout(session, user, payload.plan_code)
    return CheckoutSession(
        provider=subscription.provider,
        checkout_url=checkout_url,
        reference=subscription.provider_reference,
    )


@router.get("/subscriptions", response_model=list[SubscriptionRead])
async def subscriptions(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user.id).options(selectinload(Subscription.plan))
    )
    return list(result.scalars())
