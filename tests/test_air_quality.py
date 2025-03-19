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
    response = test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85})
    assert response.status_code == 200, f"Failed to create TestCity: {response.text}"

    time.sleep(1)

    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"
    assert "Flushed" in response.json()["message"]

def test_get_deleted_city(test_client):
    test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85})
    time.sleep(1)

    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 200, f"Failed to delete TestCity: {response.text}"

    time.sleep(1)

    response = test_client.get(f"{BASE_URL}/air-quality/TestCity")
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}: {response.text}"
    assert "Data not found" in response.json()["detail"]
