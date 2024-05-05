from fastapi.testclient import TestClient
from uuid import UUID
from main import app
from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport

"""тестирующий файл"""

client = TestClient(app)

def test_answer_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"test": "new ok"}


def uuid_is_valid(uuid_to_test):
    try:
        UUID(uuid_to_test)
        return True
    except ValueError:
        return False

def test_create_user():
    response = client.post("/create_user", json={
        "login": "кто прочитал, тому счастья и здоровья",
        "password": "69",
        "project_id": "44a842a7-6675-41fd-b1e1-291896a2f9fb",
        "env": "stage",
        "domain": "regular"
    })
    data = response.json()
    data.pop("user_id")
    correct_answer = {"created_ad":"2024-05-04",
                      "login":"кто прочитал, тому счастья и здоровья",
                      "password":"69",
                      "project_id":"44a842a7-6675-41fd-b1e1-291896a2f9fb",
                      "env":"stage",
                      "domain":"regular",
                      "locktime":0.0}
    assert response.status_code == 200
    assert data == correct_answer


@pytest.mark.asyncio
async def test_get_users():
    with patch("crud.crud_instance.get_users_db"):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
            response = await async_client.get("/get_users")
            assert response.status_code == 200
            assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_acquire_lock ():
    test_data = {"user_id": "44a842a7-6675-41fd-b1e1-291896a2f9fb"}
    
    with patch("crud.crud_instance.lock_acquire_db") as mock_db:
        mock_db.return_value = {"user": "44a842a7-6675-41fd-b1e1-291896a2f9fb", "status": "locked"}
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/release_lock", json=test_data)
            assert response.status_code == 200
            assert ("user" in response.json()) and isinstance(response.json()["user"], str)
            assert ("locktime" in response.json()) and ((response.json()["locktime"] == None)
                                                        or isinstance(response.json()["locktime"], float))
            assert ("status" in response.json()) and isinstance(response.json()["status"], str)

@pytest.mark.asyncio
async def test_release_lock():
    test_data = {"user_id": "44a842a7-6675-41fd-b1e1-291896a2f9fb"}
    
    with patch("crud.crud_instance.lock_acquire_db") as mock_db:
        mock_db.return_value = {"user": "44a842a7-6675-41fd-b1e1-291896a2f9fb", "status": "locked"}
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/acquire_lock", json=test_data)
            assert response.status_code == 200
            assert ("user" in response.json()) and isinstance(response.json()["user"], str)
            assert ("locktime" in response.json()) and ((response.json()["locktime"] == None)
                                                        or isinstance(response.json()["locktime"], float))
            assert ("status" in response.json()) and isinstance(response.json()["status"], str)
