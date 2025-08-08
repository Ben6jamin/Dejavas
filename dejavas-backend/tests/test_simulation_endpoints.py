import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _create_brief() -> str:
    payload = {
        "product_name": "Test",
        "features": [{"title": "F1", "description": "D1"}],
    }
    resp = client.post("/upload-brief/", json=payload)
    return resp.json()["session_id"]


def test_simulate_session_not_found():
    resp = client.post("/simulate/unknown")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Session not found"


def test_simulate_missing_agent_config():
    session_id = _create_brief()
    resp = client.post(f"/simulate/{session_id}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Agent configuration missing"
