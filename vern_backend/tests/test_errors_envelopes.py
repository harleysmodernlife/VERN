import json
from fastapi.testclient import TestClient
from starlette import status

from vern_backend.app.main import app

client = TestClient(app)


def test_not_found_route_envelope():
    # Call a non-existent route to trigger global handler for StarletteHTTPException 404
    resp = client.get("/__no_such_route__")
    assert resp.status_code == 404
    body = resp.json()
    assert body.get("ok") is False
    assert body.get("error_code") == "NOT_FOUND"
    assert isinstance(body.get("message"), str)


def test_validation_error_envelope_privacy_decision_missing_request_id():
    resp = client.post("/privacy/policy/decision", json={})
    # privacy_api maps missing request_id to standardized envelope (400)
    assert resp.status_code in (400, 422)
    body = resp.json()
    assert body.get("ok") is False
    assert body.get("error_code") in ("VALIDATION_ERROR",)  # FastAPI/Pydantic may return 422 via RequestValidationError
    assert isinstance(body.get("message"), str)


def test_registry_not_found_delete_nonexistent_agent():
    resp = client.delete("/agents/__nonexistent_agent__")
    assert resp.status_code == 404
    body = resp.json()
    assert body.get("ok") is False
    assert body.get("error_code") == "REGISTRY_NOT_FOUND"
    assert "not found" in body.get("message", "").lower()


def test_method_not_allowed_envelope_agents_status():
    # Use a valid route with invalid method to trigger 405 and assert envelope mapping
    resp = client.put("/agents/status")
    assert resp.status_code == 405
    body = resp.json()
    assert body.get("ok") is False
    assert body.get("error_code") in ("METHOD_NOT_ALLOWED", "UNKNOWN_ERROR")
    assert isinstance(body.get("message"), str)


def test_validation_error_envelope():
    resp = client.post("/privacy/policy/decision", json={})
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body = resp.json()
    assert body.get("ok") is False
    assert body.get("error_code") == "VALIDATION_ERROR"
    assert isinstance(body.get("message"), str)
    details = body.get("details")
    if details is not None:
        assert isinstance(details, dict)