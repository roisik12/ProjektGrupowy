from fastapi import APIRouter, HTTPException
import logging
from ..database import db
from ..models import AirQualityData

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/air-quality/{location}")
async def get_air_quality(location: str):
    try:
        logger.info(f"Fetching air quality data for {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()

        data = [doc.to_dict() for doc in docs]

        if not data:
            raise HTTPException(status_code=404, detail="Data not found")

        return {"location": location, "history": data}

    except HTTPException as http_exc:
        raise http_exc # Keep the HTTPException raised
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/air-quality/{location}")
async def set_air_quality(location: str, data: AirQualityData):
    try:
        logger.info(f"Saving air quality data for {location}")

        city_ref = db.collection("air_quality").document(location)
        city_ref.set({"location": location}, merge=True)

        doc_ref = city_ref.collection("history").document()
        doc_ref.set({"AQI": data.AQI, "last_update": data.last_update})

        return {"message": f"Data for {location} saved successfully"}

    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/air-quality/{location}")
async def flush_air_quality(location: str):
    try:
        city_ref = db.collection("air_quality").document(location)
        history_docs = city_ref.collection("history").stream()

        for doc in history_docs:
            doc.reference.delete()

        city_ref.delete()

        return {"message": f"Flushed air quality data for {location}."}
    
    except Exception as e:
        logger.error(f"Error flushing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
