import pytest
import httpx
import time
from .utils import get_firebase_token  # <-- Użyjemy tej funkcji do uzyskiwania tokenu

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def test_client():
    return httpx.Client(base_url=BASE_URL)

@pytest.fixture
def valid_token():
    """Pobiera token JWT dla testowego użytkownika"""
    return get_firebase_token("testuser@gmail.com", "Test123!")  # Możesz zmienić dane użytkownika

def test_root(test_client, valid_token):
    """Test: Sprawdzenie, czy endpoint root działa"""
    response = test_client.get("/", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Air Quality Service Running"}

def test_post_air_quality(test_client, valid_token):
    """Test: Tworzenie danych jakości powietrza z poprawnym tokenem"""
    response = test_client.post(f"{BASE_URL}/air-quality/Warsaw", json={"AQI": 85}, headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Data for Warsaw saved successfully"

def test_get_air_quality(test_client, valid_token):
    """Test: Pobieranie danych jakości powietrza z poprawnym tokenem"""
    response = test_client.get(f"{BASE_URL}/air-quality/Warsaw", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert "history" in response.json()

def test_delete_air_quality(test_client, valid_token):
    """Test: Usuwanie danych jakości powietrza z poprawnym tokenem"""
    # Tworzenie danych
    response = test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85}, headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, f"Failed to create TestCity: {response.text}"

    time.sleep(1)

    # Usuwanie danych
    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"
    assert "Flushed" in response.json()["message"]

def test_get_deleted_city(test_client, valid_token):
    """Test: Próba pobrania usuniętych danych jakości powietrza z poprawnym tokenem"""
    # Tworzenie danych
    test_client.post(f"{BASE_URL}/air-quality/TestCity", json={"AQI": 85}, headers={"Authorization": f"Bearer {valid_token}"})
    time.sleep(1)

    # Usuwanie danych
    response = test_client.delete(f"{BASE_URL}/air-quality/TestCity", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, f"Failed to delete TestCity: {response.text}"

    time.sleep(1)

    # Sprawdzanie, czy dane zostały usunięte
    response = test_client.get(f"{BASE_URL}/air-quality/TestCity", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}: {response.text}"
    assert "Data not found" in response.json()["detail"]
