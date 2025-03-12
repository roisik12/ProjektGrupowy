from google.cloud import firestore
import os

# Set Firestore authentication
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "firestore_key.json")
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

        # Check if history subcollection exists
        history_ref = db.collection("air_quality").document(doc.id).collection("history").stream()
        history_count = sum(1 for _ in history_ref)
        print(f"   └── 🔹 {history_count} historical AQI records found.")

    if not found:
        print("⚠️ No cities found in Firestore. The database may be empty.")

if __name__ == "__main__":
    check_firestore()
