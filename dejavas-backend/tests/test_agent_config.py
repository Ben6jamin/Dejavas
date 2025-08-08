import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_configure_agents_valid_percentages():
    brief_payload = {
        "product_name": "Test",
        "features": [{"title": "F1", "description": "D1"}],
    }
    upload_resp = client.post("/upload-brief/", json=brief_payload)
    session_id = upload_resp.json()["session_id"]

    config_payload = {
        "customer_percentage": 25,
        "competitor_percentage": 25,
        "influencer_percentage": 25,
        "internal_team_percentage": 25,
    }
    resp = client.post(f"/configure-agents/{session_id}", json=config_payload)
    assert resp.status_code == 200
    assert resp.json() == {"message": "Agent configuration saved"}


def test_configure_agents_invalid_percentages():
    brief_payload = {
        "product_name": "Test",
        "features": [{"title": "F1", "description": "D1"}],
    }
    upload_resp = client.post("/upload-brief/", json=brief_payload)
    session_id = upload_resp.json()["session_id"]

    config_payload = {
        "customer_percentage": 30,
        "competitor_percentage": 30,
        "influencer_percentage": 30,
        "internal_team_percentage": 30,
    }
    resp = client.post(f"/configure-agents/{session_id}", json=config_payload)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Agent percentages must sum to 100"
