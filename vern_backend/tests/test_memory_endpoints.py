import pytest
from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_memory_get():
    response = client.get("/memory")
    assert response.status_code == 200
    assert "memory" in response.json()

def test_memory_post():
    payload = {"data": "test"}
    response = client.post("/memory", json=payload)
    assert response.status_code == 200
    assert response.json().get("result") is not None