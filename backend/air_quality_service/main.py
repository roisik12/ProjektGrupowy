from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import logging
from pydantic import BaseModel, Field
from datetime import datetime

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

# FastAPI App
app = FastAPI()

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
        doc_ref = db.collection("air_quality").document(location)
        doc = doc_ref.get()

        if not doc.exists:
            logger.warning(f"Data not found for {location}")
            raise HTTPException(status_code=404, detail="Data not found")

        logger.info(f"Data retrieved for {location}: {doc.to_dict()}")
        return doc.to_dict()
    except Exception as e:
        logger.error(f"Error fetching data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/air-quality/{location}")
async def set_air_quality(location: str, data: AirQualityData):
    try:
        logger.info(f"Saving air quality data for {location}: {data}")
        doc_ref = db.collection("air_quality").document(location)
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
        doc_ref = db.collection("air_quality").document(location)

        if not doc_ref.get().exists:
            logger.warning(f"Tried to delete non-existent data for {location}")
            raise HTTPException(status_code=404, detail="Data not found")

        doc_ref.delete()
        return {"message": f"Data for {location} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting data for {location}: {e}")
        raise HTTPException(status_code=500, detail=str(e))