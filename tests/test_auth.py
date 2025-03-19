import pytest
import httpx
from .utils import get_firebase_token

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)

def test_protected_no_token(client):
    """Test: Odmowa dostępu bez tokena"""
    response = client.get(f"{BASE_URL}/protected")
    assert response.status_code == 401
    assert "Invalid Authorization Header" in response.text

def test_protected_invalid_token(client):
    """Test: Odmowa dostępu dla błędnego tokena"""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get(f"{BASE_URL}/protected", headers=headers)
    assert response.status_code == 401
    assert "Invalid Firebase token" in response.text

@pytest.fixture
def valid_token():
    """Pobiera token JWT dla testowego użytkownika"""
    return get_firebase_token("testuser@gmail.com", "Test123!")

def test_protected_valid_token(client, valid_token):
    """Test dostępu do endpointu chronionego poprawnym tokenem"""
    response = client.get("/protected", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200, f"Błąd: {response.text}"
    assert response.json()["message"] == "This is a protected API!"