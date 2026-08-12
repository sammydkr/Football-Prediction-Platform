import pytest


async def _auth_header(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "analyst@example.com", "password": "super-secret-pass"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "analyst@example.com", "password": "super-secret-pass"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.mark.asyncio
async def test_demo_ingestion_and_prediction(client):
    headers = await _auth_header(client)

    ingest = await client.post("/api/v1/matches/ingest-demo", headers=headers)
    assert ingest.status_code == 200
    assert ingest.json()["matches"] == 3

    matches = await client.get("/api/v1/matches")
    assert matches.status_code == 200
    match_id = matches.json()[0]["id"]

    prediction = await client.post(f"/api/v1/predictions/matches/{match_id}", headers=headers)
    assert prediction.status_code == 200
    body = prediction.json()
    assert body["model_version"] == "demo-elo-v1"
    total = body["home_win_probability"] + body["draw_probability"] + body["away_win_probability"]
    assert 0.99 <= total <= 1.01

    outbox = await client.get("/api/v1/events/outbox", headers=headers)
    assert outbox.status_code == 200
    assert {event["event_type"] for event in outbox.json()} >= {"match.created", "prediction.created"}

