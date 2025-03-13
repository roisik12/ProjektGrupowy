from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import logging
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import uuid4  # Generate unique document IDs
from typing import Optional
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Get the absolute path of firestore_key.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../../firestore_key.json")

# Set Firestore authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# Initialize FastAPI app
app = FastAPI()

# Initialize Firestore
db = firestore.Client()

# Validate AQI values


class AirQualityData(BaseModel):
    AQI: int = Field(..., ge=0, le=500, description="Air Quality Index must be between 0 and 500")
    last_update: Optional[str] = None  # ✅ Allow user to provide `last_update`

    @validator("last_update", pre=True, always=True)
    def set_last_update(cls, value):
        """Ensure `last_update` is correctly formatted or set to the current UTC time."""
        if not value:
            return datetime.utcnow().isoformat()  # Set current time if missing
        return value  # Otherwise, use provided timestamp

@app.get("/")
async def root():
    return {"message": "Air Quality Service Running"}

@app.get("/air-quality/{location}")
async def get_air_quality(location: str):
    try:
        logger.info(f"Fetching air quality data for {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()

        data = []
        for doc in docs:
            entry = doc.to_dict()
            data.append(entry)

        if not data:
            logger.warning(f"Data not found for {location}")
            raise HTTPException(status_code=404, detail="Data not found")  # ✅ First error raised here

        logger.info(f"Data retrieved for {location}: {data}")
        return {"location": location, "history": data}

    except HTTPException as e:
        raise e  # ✅ Keep 404 if it was already raised

    except Exception as e:
        logger.error(f"Unexpected error fetching data for {location}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")  # ✅ Only trigger 500 for real errors



@app.post("/air-quality/{location}")
async def set_air_quality(location: str, data: AirQualityData):
    try:
        logger.info(f"Saving air quality data for {location}: {data}")

        # ✅ `last_update` is now extracted properly from the request
        last_update = data.last_update

        # Ensure a document exists for the location
        city_ref = db.collection("air_quality").document(location)
        city_ref.set({"location": location}, merge=True)  # Prevents overwriting

        # ✅ Store `last_update` properly in Firestore
        doc_ref = city_ref.collection("history").document()
        doc_ref.set({
            "AQI": data.AQI,
            "last_update": last_update  # ✅ Will now store user-provided `last_update`
        })

        return {"message": f"Data for {location} saved successfully"}
    
    except Exception as e:
        logger.error(f"Error saving data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/air-quality/{location}")
async def flush_air_quality(location: str):
    try:
        logger.info(f"Flushing air quality data for {location}...")

        city_ref = db.collection("air_quality").document(location)

        # Fetch the document without using a transaction
        city_doc = city_ref.get()

        # Check if the city document exists
        if not city_doc.exists:
            logger.warning(f"Location {location} not found in Firestore.")
            raise HTTPException(status_code=404, detail=f"Location {location} not found.")

        # Delete all records in the "history" subcollection
        history_docs = city_ref.collection("history").stream()
        deleted_count = 0
        for doc in history_docs:
            doc.reference.delete()
            deleted_count += 1

        # Delete the main city document after deleting history
        city_ref.delete()
        deleted_count += 1

        logger.info(f"Deleted {deleted_count} records for {location}.")
        return {"message": f"Flushed {deleted_count} records for {location}."}
    
    except Exception as e:
        logger.error(f"Error flushing data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


