
import pytest
from httpx import AsyncClient
from fastapi import Depends
from main import app
from utils.security import get_current_user

# --- Mock user dependency (Admin role) ---
def override_get_current_user():
    return {
        "username": "admin@example.com",
        "role": "Admin",
        "tenant": "tenant1"
    }

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_get_tenant_config():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/api/tenant/config")
        assert res.status_code == 200
        assert "features" in res.json()
        assert "primaryColor" in res.json()

@pytest.mark.asyncio
async def test_update_tenant_config():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.put("/api/tenant/config", json={
            "primaryColor": "#123456"
        })
        assert res.status_code == 200
        assert res.json()["primaryColor"] == "#123456"

@pytest.mark.asyncio
async def test_get_tenant_features():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/api/tenant/features")
        assert res.status_code == 200
        assert isinstance(res.json(), dict)

@pytest.mark.asyncio
async def test_update_tenant_features():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.put("/api/tenant/features", json={
            "features": {
                "feature1": True,
                "feature2": False
            }
        })
        assert res.status_code == 200
        assert res.json()["feature1"] is True
