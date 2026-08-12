import asyncio

from app.db.session import SessionLocal
from app.services.events import RedisEventPublisher, publish_pending_outbox


async def main() -> None:
    publisher = RedisEventPublisher()
    try:
        while True:
            async with SessionLocal() as session:
                await publish_pending_outbox(session, publisher)
            await asyncio.sleep(2)
    finally:
        await publisher.close()


if __name__ == "__main__":
    asyncio.run(main())

