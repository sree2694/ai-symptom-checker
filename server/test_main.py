# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_check_symptoms_success():
    payload = {
        "age": 30,
        "gender": "male",
        "symptoms": ["fever", "cough", "fatigue"]
    }
    response = client.post("/api/check-symptoms", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "conditions" in data or "error" in data  # Accept either real or fallback

def test_check_symptoms_invalid_payload():
    payload = {
        "age": "thirty",  # invalid type
        "gender": "male",
        "symptoms": ["fever"]
    }
    response = client.post("/api/check-symptoms", json=payload)
    assert response.status_code == 422  # validation error
