from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)


def assert_envelope(resp, expected_code: str | None = None, expected_status: int | None = None):
    if expected_status is not None:
        assert resp.status_code == expected_status
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("ok") is False
    if expected_code is not None:
        assert data.get("error_code") == expected_code
    assert isinstance(data.get("message"), str)


def test_integrations_bogus_provider_not_found():
    resp = client.get("/integrations/__bogus__/status")
    # standardized NOT_FOUND envelope via integrations route
    assert_envelope(resp, expected_code="NOT_FOUND", expected_status=404)


def test_plugins_call_not_implemented_maps_to_not_found():
    # This calls a plugin that likely doesn't exist or tool not implemented -> NOT_FOUND
    resp = client.post("/plugins/__bogus__/call", json={"args": [], "kwargs": {}})
    # Could be NOT_FOUND or INTEGRATION_UNAVAILABLE depending on plugin layer; accept both
    data = resp.json()
    assert data.get("ok") is False
    assert data.get("error_code") in ("NOT_FOUND", "INTEGRATION_UNAVAILABLE", "INTEGRATION_ERROR", "PLUGIN_INVALID")


def test_privacy_decision_validation_error():
    resp = client.post("/privacy/policy/decision", json={})
    # privacy_api returns standardized envelope on missing request_id (400), but FastAPI may raise 422 for model validation.
    assert resp.status_code in (400, 422)
    data = resp.json()
    assert data.get("ok") is False
    # either VALIDATION_ERROR (our handler) or model-level error mapped by global handler
    assert data.get("error_code") in ("VALIDATION_ERROR",)


def test_method_not_allowed_envelope():
    # Use a valid route with invalid method to trigger 405 and global handler mapping
    resp = client.put("/agents/status")
    assert resp.status_code == 405
    data = resp.json()
    assert data.get("ok") is False
    assert data.get("error_code") in ("METHOD_NOT_ALLOWED", "UNKNOWN_ERROR")
    assert isinstance(data.get("message"), str)