from datetime import UTC, datetime

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.events import OutboxEvent


async def add_outbox_event(
    session: AsyncSession,
    *,
    event_type: str,
    aggregate_type: str,
    aggregate_id: str | int,
    payload: dict,
) -> OutboxEvent:
    event = OutboxEvent(
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=str(aggregate_id),
        payload=payload,
    )
    session.add(event)
    return event


class RedisEventPublisher:
    def __init__(self, redis: Redis | None = None) -> None:
        self.redis = redis or Redis.from_url(settings.redis_url, decode_responses=True)

    async def publish(self, event: OutboxEvent) -> None:
        await self.redis.publish(settings.event_channel, event_payload(event))

    async def close(self) -> None:
        await self.redis.aclose()


def event_payload(event: OutboxEvent) -> str:
    import json

    return json.dumps(
        {
            "id": event.id,
            "type": event.event_type,
            "aggregate_type": event.aggregate_type,
            "aggregate_id": event.aggregate_id,
            "payload": event.payload,
            "created_at": event.created_at.isoformat(),
        },
        sort_keys=True,
    )


async def publish_pending_outbox(session: AsyncSession, publisher: RedisEventPublisher) -> int:
    result = await session.execute(
        select(OutboxEvent).where(OutboxEvent.status == "pending").order_by(OutboxEvent.id).limit(100)
    )
    events = list(result.scalars())
    for event in events:
        event.attempts += 1
        await publisher.publish(event)
        event.status = "published"
        event.published_at = datetime.now(UTC)
    await session.commit()
    return len(events)

