import os
import logging
from google.cloud import firestore

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIRESTORE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "../firestore_key.json")

# Set Firestore credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = FIRESTORE_CREDENTIALS_PATH

# Initialize Firestore client
db = firestore.Client()

def get_history_data(location: str):
    """
    Retrieve historical air quality data for the given location from Firestore.
    Returns a list of dictionaries, each containing at least:
      - "AQI"
      - "last_update"
    """
    try:
        logger.info(f"Fetching historical data for location: {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()
        data = [doc.to_dict() for doc in docs]
        logger.info(f"Found {len(data)} data points for {location}")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {location}: {e}")
        return []
