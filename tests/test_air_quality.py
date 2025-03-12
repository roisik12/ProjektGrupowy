import pytest
import httpx
import time

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def test_client():
    return httpx.Client(base_url=BASE_URL)

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Air Quality Service Running"}

def test_post_air_quality(test_client):
    response = test_client.post(f"{BASE_URL}/air-quality/Warsaw", json={"AQI": 85})
    assert response.status_code == 200
    assert response.json()["message"] == "Data for Warsaw saved successfully"

def test_get_air_quality(test_client):
    response = test_client.get(f"{BASE_URL}/air-quality/Warsaw")
    assert response.status_code == 200
    assert "history" in response.json()

def test_delete_air_quality(test_client):
    # Ensure city exists before deleting
    response = test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85})
    assert response.status_code == 200, f"Failed to create TestCity: {response.text}"

    # Wait to ensure Firestore processes the new entry
    time.sleep(1)

    # Now try deleting
    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"
    assert "Flushed" in response.json()["message"]

def test_get_deleted_city(test_client):
    # Ensure city exists before deletion
    test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85})
    time.sleep(1)  # Wait for Firestore to process

    # Delete the city
    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 200, f"Failed to delete TestCity: {response.text}"

    # Wait for Firestore to process deletion
    time.sleep(1)

    # ✅ FIX: Ensure `GET /air-quality/TestCity` correctly returns `404`
    response = test_client.get(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}: {response.text}"
    assert "Data not found" in response.json()["detail"]
