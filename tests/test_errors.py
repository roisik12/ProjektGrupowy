import pytest
from fastapi.testclient import TestClient
from backend.air_quality_service.main import app
from backend.air_quality_service.database import get_firestore_client
from .utils import get_firebase_token  # <-- Zaimportuj funkcję do pobierania tokenu

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def valid_token():
    """Pobiera token JWT dla testowego użytkownika"""
    return get_firebase_token("testuser@gmail.com", "Test123!")  # Zmien dane na testowego użytkownika

class MockFirestoreClient:
    """Mock Firestore client that raises an error when trying to fetch data."""

    def collection(self, name):
        return self  # Simulate collection reference

    def document(self, name):
        return self  # Simulate document reference

    def get(self):
        raise Exception("🔥 Simulated Firestore failure")  # Force internal error

@pytest.fixture
def override_firestore():
    """Override Firestore client with a failing mock"""
    app.dependency_overrides[get_firestore_client] = lambda: MockFirestoreClient()
    yield
    app.dependency_overrides.clear()  # Reset after test

def test_air_quality_internal_error(client, override_firestore):
    """Test API error handling by injecting a failing Firestore client."""
    
    response = client.get(f"{BASE_URL}/air-quality/Warsaw")

    assert response.status_code == 500  # ✅ Should return 500 Internal Server Error
    assert "Internal Server Error" in response.text

def test_air_quality_not_found(client, valid_token):
    """Test: Requesting air quality data for a city that doesn't exist."""
    
    response = client.get(f"/air-quality/NonExistentCity", headers={"Authorization": f"Bearer {valid_token}"})
    
    assert response.status_code == 404  # ✅ Should return 404 Not Found
    assert "Data not found" in response.text

def test_air_quality_invalid_post(client, valid_token):
    """Test: Sending an invalid payload to POST (missing AQI value)."""
    
    response = client.post(f"/air-quality/Warsaw", json={}, headers={"Authorization": f"Bearer {valid_token}"})
    
    assert response.status_code == 422  # ✅ Should return 422 Unprocessable Entity
    assert "AQI" in response.text  # ✅ Should mention missing AQI

def test_air_quality_delete_non_existent(client, valid_token):
    """Test: Attempting to delete a non-existent location should still work (idempotency)."""
    
    response = client.delete(f"/air-quality/NonExistentCity", headers={"Authorization": f"Bearer {valid_token}"})
    
    assert response.status_code == 200
    assert "Flushed air quality data" in response.text

def test_air_quality_invalid_method(client):
    """Test: Sending a PUT request to an endpoint that only supports GET, POST, DELETE."""
    
    response = client.put(f"/air-quality/Warsaw", json={"AQI": 50, "last_update": "2024-06-01T12:00:00Z"})
    
    assert response.status_code == 405  # ✅ Should return 405 Method Not Allowed
    assert "Method Not Allowed" in response.text
