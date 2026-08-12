import pytest


@pytest.mark.asyncio
async def test_demo_billing_flow(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "buyer@example.com", "password": "super-secret-pass"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "buyer@example.com", "password": "super-secret-pass"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    plans = await client.get("/api/v1/billing/plans")
    assert plans.status_code == 200
    assert [plan["code"] for plan in plans.json()] == ["free", "pro"]

    checkout = await client.post("/api/v1/billing/checkout", json={"plan_code": "pro"}, headers=headers)
    assert checkout.status_code == 200
    assert checkout.json()["provider"] == "demo"

    subscriptions = await client.get("/api/v1/billing/subscriptions", headers=headers)
    assert subscriptions.status_code == 200
    assert subscriptions.json()[0]["plan"]["code"] == "pro"

