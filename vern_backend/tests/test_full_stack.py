"""
Full-stack integration tests for VERN backend:
- RAG API
- Privacy Agent API
- Multi-Agent Orchestration
- Voice/Vision Agent APIs
- Protocol Handlers
"""

from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_rag_add_and_query():
    docs = ["VERN supports RAG", "Agents use Haystack"]
    meta = [{"type": "info"}, {"type": "tech"}]
    add_resp = client.post("/rag/add", json={"docs": docs, "meta": meta})
    assert add_resp.status_code == 200
    query_resp = client.get("/rag/query", params={"query": "RAG support", "top_k": 2})
    assert query_resp.status_code == 200
    results = query_resp.json()["results"]
    assert any("VERN supports RAG" in r["content"] for r in results)

def test_privacy_agent_endpoints():
    # Check permission
    resp = client.post("/privacy/check_permission", json={
        "action": "send_email",
        "user_id": "user_1",
        "data": {"email": "alice@example.com", "ssn": "123-45-6789"}
    })
    assert resp.status_code == 200
    assert "allowed" in resp.json()
    # Sanitize data
    resp2 = client.post("/privacy/sanitize", json={
        "data": {"email": "alice@example.com", "ssn": "123-45-6789", "credit_card": "4111111111111111"}
    })
    assert resp2.status_code == 200
    sanitized = resp2.json()["sanitized"]
    assert "ssn" not in sanitized and "credit_card" not in sanitized
    # Audit log
    resp3 = client.get("/privacy/audit_log")
    assert resp3.status_code == 200
    assert isinstance(resp3.json()["audit_log"], list)

def test_orchestrate_agents():
    resp = client.post("/agents/orchestrate", json={"task": "Plan a trip", "context": {}})
    assert resp.status_code == 200
    data = resp.json()
    assert "steps" in data and "results" in data and "critiques" in data

def test_voice_agent_stub():
    # Direct import test (not API)
    from src.mvp.voice_agent import transcribe_audio, synthesize_speech
    assert transcribe_audio(b"audio") == "Transcribed text (stub)"
    assert synthesize_speech("Hello world") == b"audio-bytes-stub"

def test_vision_agent_stub():
    from src.mvp.vision_agent import analyze_image, extract_text_from_document
    result = analyze_image(b"image")
    assert "caption" in result and "labels" in result
    text = extract_text_from_document(b"doc")
    assert "Extracted text" in text

def test_protocol_handlers():
    from src.mvp.protocols import handle_mcp_message, handle_grpc_request
    mcp_resp = handle_mcp_message({"type": "call_tool", "tool": "weather", "params": {"location": "Austin"}})
    assert mcp_resp["status"] == "ok"
    grpc_resp = handle_grpc_request({"method": "AgentService/Call", "payload": {"agent": "planner"}})
    assert grpc_resp["status"] == "ok"
