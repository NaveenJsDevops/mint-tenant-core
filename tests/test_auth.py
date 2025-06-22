
import pytest
from httpx import AsyncClient
from fastapi import Depends
from main import app
from utils.security import get_current_user

# --- Mock user dependency ---
def override_get_current_user():
    return {
        "username": "testuser@example.com",
        "role": "HR",
        "tenant": "tenant1"
    }

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ping")
        assert response.status_code == 200
        assert response.json()["message"] == "pong"

@pytest.mark.asyncio
async def test_auth_me():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/auth/me")
        assert response.status_code == 200
        assert "username" in response.json()
        assert "tenant" in response.json()
