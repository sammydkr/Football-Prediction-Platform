import pytest


@pytest.mark.asyncio
async def test_register_login_and_refresh(client):
    register = await client.post(
        "/api/v1/auth/register",
        json={"email": "demo@example.com", "password": "correct horse battery"},
    )
    assert register.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "correct horse battery"},
    )
    assert login.status_code == 200
    tokens = login.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]

    refresh = await client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refresh.status_code == 200
    assert refresh.json()["refresh_token"] != tokens["refresh_token"]

