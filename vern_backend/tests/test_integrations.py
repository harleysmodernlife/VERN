from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_list_integrations():
    resp = client.get("/integrations/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(i["provider"] == "google_calendar" for i in data)
    assert any(i["provider"] == "openweathermap" for i in data)

def test_get_integration_status():
    resp = client.get("/integrations/google_calendar/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["provider"] == "google_calendar"
    assert not data["configured"]

def test_configure_integration_missing_keys():
    resp = client.post("/integrations/google_calendar/configure", json={"config": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert not data["configured"]

def test_configure_integration_success():
    keys = {
        "GOOGLE_CALENDAR_ID": "fake_id",
        "GOOGLE_CALENDAR_CREDENTIALS_JSON": "fake.json"
    }
    resp = client.post("/integrations/google_calendar/configure", json={"config": keys})
    assert resp.status_code == 200
    data = resp.json()
    assert data["configured"]
