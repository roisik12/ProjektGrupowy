import pytest
import httpx
import time
import random
from datetime import datetime, timedelta, timezone  

BASE_URL = "http://127.0.0.1:8002"
AIR_QUALITY_URL = "http://127.0.0.1:8001"

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
    """Test prediction using random AQI values for TestCity with valid timestamps."""

    aqi_values = [random.randint(50, 150) for _ in range(5)]
    start_time = datetime.now() - timedelta(days=5)


    for i, aqi in enumerate(aqi_values):
        last_update = (start_time + timedelta(days=i)).isoformat()
        add_data = httpx.post(
            f"{AIR_QUALITY_URL}/air-quality/TestCity",
            json={"AQI": aqi, "last_update": last_update},
        )
        assert add_data.status_code == 200, f"Failed to add AQI data: {add_data.text}"

    time.sleep(1)

    response = test_client.get(f"{BASE_URL}/predict/TestCity")
    assert response.status_code == 200, f"Unexpected response: {response.status_code} - {response.text}"
    
    predicted_aqi = response.json()["predicted_AQI"]
    assert 0 <= predicted_aqi <= 500, f"Predicted AQI out of range: {predicted_aqi}"

    delete_data = httpx.delete(f"{AIR_QUALITY_URL}/air-quality/TestCity")
    assert delete_data.status_code == 200, f"Failed to delete TestCity: {delete_data.text}"