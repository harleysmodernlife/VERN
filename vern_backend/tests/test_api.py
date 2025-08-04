from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_get_env():
    response = client.get("/config/env")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_validate_env():
    response = client.get("/config/validate")
    assert response.status_code == 200
    assert "missing" in response.json()
    assert "placeholders" in response.json()

def test_list_plugins():
    response = client.get("/plugins/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_run_workflow():
    # Create workflow
    workflow = {
        "name": "test_workflow",
        "steps": [
            {"agent": "research", "input": "test input"}
        ]
    }
    create_resp = client.post("/agents/workflows/create", json=workflow)
    assert create_resp.status_code == 200
    # List workflows
    list_resp = client.get("/agents/workflows/list")
    assert list_resp.status_code == 200
    assert "test_workflow" in list_resp.json()
    # Run workflow
    run_resp = client.post("/agents/workflows/run", json={"name": "test_workflow"})
    assert run_resp.status_code == 200
    assert "result" in run_resp.json()

def test_run_nonexistent_workflow():
    run_resp = client.post("/agents/workflows/run", json={"name": "does_not_exist"})
    assert run_resp.status_code != 200
    assert "error" in run_resp.json() or "not found" in run_resp.text.lower()

def test_create_workflow_invalid_payload():
    # Missing steps
    workflow = {"name": "bad_workflow"}
    create_resp = client.post("/agents/workflows/create", json=workflow)
    assert create_resp.status_code != 200

def test_plugin_api_invalid_plugin():
    resp = client.post("/plugins/bogus_plugin/call", json={"params": {}})
    assert resp.status_code != 200
    assert "detail" in resp.json() or "not found" in resp.text.lower()
