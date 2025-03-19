import pytest
from fastapi.testclient import TestClient
from backend.air_quality_service.main import app
from backend.air_quality_service.database import get_firestore_client

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

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
def test_air_quality_not_found(client):
    """Test: Requesting air quality data for a city that doesn't exist."""
    
    response = client.get(f"/air-quality/NonExistentCity")
    
    assert response.status_code == 404  # ✅ Should return 404 Not Found
    assert "Data not found" in response.text


def test_air_quality_invalid_post(client):
    """Test: Sending an invalid payload to POST (missing AQI value)."""
    
    response = client.post(f"/air-quality/Warsaw", json={})
    
    assert response.status_code == 422  # ✅ Should return 422 Unprocessable Entity
    assert "AQI" in response.text  # ✅ Should mention missing AQI


def test_air_quality_delete_non_existent(client):
    """Test: Attempting to delete a non-existent location should still work (idempotency)."""
    
    response = client.delete(f"/air-quality/NonExistentCity")
    
    assert response.status_code == 200  # ✅ Should return 200 even if nothing was deleted
    assert "Flushed air quality data" in response.text


def test_air_quality_invalid_method(client):
    """Test: Sending a PUT request to an endpoint that only supports GET, POST, DELETE."""
    
    response = client.put(f"/air-quality/Warsaw", json={"AQI": 50, "last_update": "2024-06-01T12:00:00Z"})
    
    assert response.status_code == 405  # ✅ Should return 405 Method Not Allowed
    assert "Method Not Allowed" in response.text