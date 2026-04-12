import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "up"

def test_voice_instruct_no_patient():
    # Simulate Africa's Talking hitting the webhook for an unknown number
    response = client.post(
        "/voice/instruct",
        data={
            "sessionId": "mock123",
            "direction": "Outbound",
            "destinationNumber": "+254000000000"
        }
    )
    assert response.status_code == 200
    assert "Sorry" in response.text
    assert "<Response>" in response.text
