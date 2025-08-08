import pytest
from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_orchestrator_status():
    response = client.get("/orchestrator/status")
    assert response.status_code == 200
    assert "status" in response.json()

def test_orchestrator_action():
    payload = {"action": "ping"}
    response = client.post("/orchestrator/action", json=payload)
    assert response.status_code == 200
    assert response.json().get("result") is not None