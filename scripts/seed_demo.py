import asyncio

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.demo_provider import DemoSportsDataProvider
from app.services.ingestion import ingest_snapshot
from app.services.payments import ensure_default_plans


async def main() -> None:
    async with SessionLocal() as session:
        await ensure_default_plans(session)
        provider = DemoSportsDataProvider(settings.demo_provider_seed)
        result = await ingest_snapshot(session, await provider.fetch_snapshot())
        print(f"Seeded demo data: {result}")


if __name__ == "__main__":
    asyncio.run(main())

