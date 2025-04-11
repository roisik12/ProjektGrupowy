import os
import logging
from google.cloud import firestore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FIRESTORE_CREDENTIALS_PATH = (
    os.environ.get("FIRESTORE_CREDENTIALS_PATH") or
    os.path.join(BASE_DIR, "../firestore_key.json")
)

# ✅ Tworzymy klienta Firestore bez zmieniania globalnego środowiska
db = firestore.Client.from_service_account_json(FIRESTORE_CREDENTIALS_PATH)

def get_firestore_client():
    """Return Firestore client instance (for dependency injection in tests)"""
    return db

def get_air_quality_data(location: str):
    """Retrieve air quality data from Firestore"""
    try:
        logger.info(f"Fetching air quality data for {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None

def save_air_quality_data(location: str, aqi: int, last_update: str):
    """Save air quality data to Firestore"""
    city_ref = db.collection("air_quality").document(location)
    city_ref.set({"location": location}, merge=True)
    doc_ref = city_ref.collection("history").document()
    doc_ref.set({"AQI": aqi, "last_update": last_update})
