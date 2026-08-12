from datetime import UTC, datetime, timedelta
from random import Random


class DemoSportsDataProvider:
    def __init__(self, seed: int = 2026) -> None:
        self.random = Random(seed)

    async def fetch_snapshot(self) -> dict:
        teams = [
            {"provider_id": "ars", "name": "Arsenal", "short_name": "ARS"},
            {"provider_id": "che", "name": "Chelsea", "short_name": "CHE"},
            {"provider_id": "liv", "name": "Liverpool", "short_name": "LIV"},
            {"provider_id": "mci", "name": "Manchester City", "short_name": "MCI"},
        ]
        now = datetime.now(UTC).replace(microsecond=0)
        fixtures = []
        for index, (home, away) in enumerate([("ars", "che"), ("liv", "mci"), ("che", "liv")], start=1):
            fixtures.append(
                {
                    "provider_id": f"demo-{index}",
                    "competition_provider_id": "epl",
                    "home_team_provider_id": home,
                    "away_team_provider_id": away,
                    "kickoff_at": now + timedelta(days=index),
                    "status": "scheduled",
                    "home_score": None,
                    "away_score": None,
                }
            )
        return {
            "competitions": [{"provider_id": "epl", "name": "Premier League", "country": "England"}],
            "teams": teams,
            "matches": fixtures,
        }

