from google.cloud import firestore
import os
from datetime import datetime

# Set Firestore authentication
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "backend/firestore_key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# Initialize Firestore
db = firestore.Client()

def check_firestore():
    print("🔥 Checking Firestore Structure...\n")

    collection_ref = db.collection("air_quality").stream()

    found = False  # Track if any cities exist
    for doc in collection_ref:
        found = True
        print(f"📌 Found City: {doc.id}")
        
        # Get city document data
        city_data = doc.to_dict()
        print(f"   ├── Name: {city_data.get('name', 'Not set')}")
        print(f"   ├── Last Update: {city_data.get('last_update', 'Not set')}")

        # Check history subcollection
        history_ref = (db.collection("air_quality")
                      .document(doc.id)
                      .collection("history")
                      .order_by("last_update", direction="DESCENDING")
                      .stream())
        
        history_docs = list(history_ref)
        print(f"   └── 🔹 {len(history_docs)} historical AQI records:")
        
        for hist_doc in history_docs:
            data = hist_doc.to_dict()
            print(f"       ├── AQI: {data.get('AQI', 'No AQI')}")
            print(f"       ├── Time: {data.get('last_update', 'No timestamp')}")
            print(f"       ├── Source: {data.get('source', 'No source')}")
            
            # Print raw data if available
            raw_data = data.get('raw_data', {})
            if raw_data:
                print(f"       └── Raw Data:")
                for key, value in raw_data.items():
                    print(f"           ├── {key}: {value}")
            print()

    if not found:
        print("⚠️ No cities found in Firestore. The database may be empty.")

if __name__ == "__main__":
    check_firestore()
