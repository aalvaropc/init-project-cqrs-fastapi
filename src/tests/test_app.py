import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_create_user():
    user_data = {"username": "testuser", "password": "testpass"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"