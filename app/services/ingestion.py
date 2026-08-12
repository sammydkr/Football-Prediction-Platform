from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.matches import Competition, Match, Team
from app.services.events import add_outbox_event


async def ingest_snapshot(session: AsyncSession, snapshot: dict) -> dict[str, int]:
    counts = {"competitions": 0, "teams": 0, "matches": 0}
    competitions: dict[str, Competition] = {}
    teams: dict[str, Team] = {}

    for item in snapshot["competitions"]:
        competition = await session.scalar(
            select(Competition).where(Competition.provider_id == item["provider_id"])
        )
        if not competition:
            competition = Competition(**item)
            session.add(competition)
            counts["competitions"] += 1
        else:
            competition.name = item["name"]
            competition.country = item["country"]
        competitions[item["provider_id"]] = competition

    for item in snapshot["teams"]:
        team = await session.scalar(select(Team).where(Team.provider_id == item["provider_id"]))
        if not team:
            team = Team(**item)
            session.add(team)
            counts["teams"] += 1
        else:
            team.name = item["name"]
            team.short_name = item["short_name"]
        teams[item["provider_id"]] = team

    await session.flush()

    for item in snapshot["matches"]:
        match = await session.scalar(select(Match).where(Match.provider_id == item["provider_id"]))
        payload = {
            "provider_id": item["provider_id"],
            "status": item["status"],
            "kickoff_at": item["kickoff_at"].isoformat(),
        }
        if not match:
            match = Match(
                provider_id=item["provider_id"],
                competition_id=competitions[item["competition_provider_id"]].id,
                home_team_id=teams[item["home_team_provider_id"]].id,
                away_team_id=teams[item["away_team_provider_id"]].id,
                kickoff_at=item["kickoff_at"],
                status=item["status"],
                home_score=item["home_score"],
                away_score=item["away_score"],
            )
            session.add(match)
            counts["matches"] += 1
            event_type = "match.created"
        else:
            match.kickoff_at = item["kickoff_at"]
            match.status = item["status"]
            match.home_score = item["home_score"]
            match.away_score = item["away_score"]
            match.updated_at = datetime.now(UTC)
            event_type = "match.updated"
        await session.flush()
        await add_outbox_event(
            session,
            event_type=event_type,
            aggregate_type="match",
            aggregate_id=match.id,
            payload=payload,
        )

    await session.commit()
    return counts

