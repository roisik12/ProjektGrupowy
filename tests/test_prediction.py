import pytest
import httpx

BASE_URL = "http://127.0.0.1:8002"

@pytest.fixture
def test_client():
    return httpx.Client(base_url=BASE_URL)

def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Prediction Service Running"}

def test_predict_no_data(test_client):
    response = test_client.get(f"{BASE_URL}/predict/NonExistentCity")
    assert response.status_code in [400, 500], f"Unexpected response: {response.status_code} - {response.text}"
    assert "Not enough historical data" in response.json()["detail"]

def test_predict_air_quality(test_client):
    # Ensure there is data for "Paris" before testing
    add_data = httpx.post(f"http://127.0.0.1:8001/air-quality/Paris", json={"AQI": 95})
    assert add_data.status_code == 200
    add_data = httpx.post(f"http://127.0.0.1:8001/air-quality/Paris", json={"AQI": 115})
    assert add_data.status_code == 200
    add_data = httpx.post(f"http://127.0.0.1:8001/air-quality/Paris", json={"AQI": 85})
    assert add_data.status_code == 200
    add_data = httpx.post(f"http://127.0.0.1:8001/air-quality/Paris", json={"AQI": 99})
    assert add_data.status_code == 200
    add_data = httpx.post(f"http://127.0.0.1:8001/air-quality/Paris", json={"AQI": 95})
    assert add_data.status_code == 200

    response = test_client.get(f"{BASE_URL}/predict/Paris")
    assert response.status_code == 200, f"Unexpected response: {response.status_code} - {response.text}"
    assert 0 <= response.json()["predicted_AQI"] <= 500  # Ensure AQI is within valid range
