import pytest
import httpx
import time

BASE_URL = "http://127.0.0.1:8001"

@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)

def test_air_quality_response_time(client):
    """Test: API powinno odpowiadać w czasie < 0.5s"""
    start_time = time.time()
    response = client.get(f"{BASE_URL}/air-quality/Warsaw")
    elapsed_time = time.time() - start_time

    assert response.status_code in [200, 404]  # API może zwrócić dane lub brak danych
    assert elapsed_time < 0.5, f"API response time is too slow: {elapsed_time:.3f}s"

def test_high_load(client):
    """Test: API pod dużym obciążeniem"""
    requests = 50  # Liczba żądań
    slow_responses = 0

    for _ in range(requests):
        start_time = time.time()
        response = client.get(f"{BASE_URL}/air-quality/Warsaw")
        elapsed_time = time.time() - start_time

        if elapsed_time > 0.5:
            slow_responses += 1

    assert slow_responses < 5, f"Too many slow responses ({slow_responses}/{requests})"
