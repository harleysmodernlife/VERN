from fastapi.testclient import TestClient
from vern_backend.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "VERN Backend API is running."}
