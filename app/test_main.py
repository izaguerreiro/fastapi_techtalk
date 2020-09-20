import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)
pytestmark = pytest.mark.asyncio


def test_search_address_not_found():
    response = client.get("/address/12420-339")
    assert response.status_code == 404
    assert response.json()["message"] == "Cep não encontrado"


def test_search_address():
    response = client.get("/address/12420-330")
    assert response.status_code == 200
    assert "cep" in response.json()


@pytest.mark.asyncio
async def test_async_search_address():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/address/12420-330")
    assert response.status_code == 200
