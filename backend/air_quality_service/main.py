from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import logging
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4  # Generate unique document IDs

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Get the absolute path of firestore_key.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../firestore_key.json")

# Set Firestore authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# Initialize FastAPI app
app = FastAPI()

# Initialize Firestore
db = firestore.Client()

# Validate AQI values
class AirQualityData(BaseModel):
    AQI: int = Field(..., ge=0, le=500, description="Air Quality Index must be between 0 and 500")

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
            raise HTTPException(status_code=404, detail="Data not found")

        logger.info(f"Data retrieved for {location}: {data}")
        return {"location": location, "history": data}
    except Exception as e:
        logger.error(f"Error fetching data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/air-quality/{location}")
async def set_air_quality(location: str, data: AirQualityData):
    try:
        logger.info(f"Saving air quality data for {location}: {data}")
        doc_ref = db.collection("air_quality").document(location).collection("history").document(str(uuid4()))
        doc_ref.set({
            "AQI": data.AQI,
            "last_update": datetime.utcnow().isoformat()
        })
        return {"message": f"Data for {location} saved successfully"}
    except Exception as e:
        logger.error(f"Error saving data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/air-quality/{location}")
async def delete_air_quality(location: str):
    try:
        logger.info(f"Deleting air quality data for {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()

        deleted_count = 0
        for doc in docs:
            doc.reference.delete()
            deleted_count += 1

        if deleted_count == 0:
            logger.warning(f"Tried to delete non-existent data for {location}")
            raise HTTPException(status_code=404, detail="Data not found")

        return {"message": f"Deleted {deleted_count} records for {location}"}
    except Exception as e:
        logger.error(f"Error deleting data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
