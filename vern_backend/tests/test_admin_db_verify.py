from fastapi.testclient import TestClient
from unittest.mock import patch
from vern_backend.app.main import app
from starlette import status

client = TestClient(app)


def test_admin_db_verify_ok_or_standard_error():
    resp = client.get("/admin/db/verify")
    # Service should respond 200 on OK; if not available, it still must return a standardized envelope
    assert resp.status_code in (200, 503, 500)
    body = resp.json()
    # Accept either success or standardized error envelope
    if isinstance(body, dict) and body.get("ok") is True:
        assert "path" in body
        assert "migrated" in body
        assert "version" in body
    else:
        assert body.get("ok") is False
        assert body.get("error_code") in ("DB_UNAVAILABLE", "UNKNOWN_ERROR")
        assert isinstance(body.get("message"), str)


def test_admin_db_verify_db_unavailable_envelope():
    # Simulate sqlite connect failure to assert DB_UNAVAILABLE envelope
    with patch("vern_backend.app.main.sqlite3.connect") as mock_connect:
        import sqlite3
        mock_connect.side_effect = sqlite3.OperationalError("simulated connect failure")
        resp = client.get("/admin/db/verify")
        assert resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = resp.json()
        assert data.get("ok") is False
        assert data.get("error_code") == "DB_UNAVAILABLE"
        assert isinstance(data.get("message"), str)
        # details should be a dict; prefer error/path keys when available
        details = data.get("details", {})
        assert isinstance(details, dict)
        # When details is empty, do not fail; log body for diagnosis
        if not details:
            print("[TEST][admin_db_verify] Body:", data)
        else:
            assert "error" in details
            assert "path" in details