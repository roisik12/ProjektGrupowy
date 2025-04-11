from fastapi import APIRouter, HTTPException, Depends, Request
import logging
from backend.air_quality_service.database import db, get_firestore_client # Changed import
from backend.air_quality_service.models import AirQualityData # Changed import
from backend.air_quality_service.auth import admin_only, verify_firebase_token as verify_token
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# GET request: Pobieranie danych o jakości powietrza
@router.get("/air-quality/{location}")
@limiter.limit("10/minute")
async def get_air_quality(request: Request, location: str, db=Depends(get_firestore_client)):
    try:
        logger.info(f"Fetching air quality data for {location}")
        docs = db.collection("air_quality").document(location).collection("history").stream()

        data = [doc.to_dict() for doc in docs]

        if not data:
            raise HTTPException(status_code=404, detail="Data not found")

        return {"location": location, "history": data}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST request: Zapis danych o jakości powietrza
@router.post("/air-quality/{location}")
@limiter.limit("5/minute")
async def set_air_quality(request: Request, location: str, data: AirQualityData, user=Depends(admin_only), db=Depends(get_firestore_client)):
    try:
        logger.info(f"[{user['email']}] is saving AQI data for {location}")
        logger.info(f"Saving air quality data for {location}")

        city_ref = db.collection("air_quality").document(location)
        city_ref.set({"location": location}, merge=True)

        doc_ref = city_ref.collection("history").document()
        doc_ref.set({"AQI": data.AQI, "last_update": data.last_update})

        return {"message": f"Data for {location} saved successfully"}

    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# DELETE request: Usuwanie danych o jakości powietrza
@router.delete("/air-quality/{location}")
async def flush_air_quality(location: str, user=Depends(admin_only), db=Depends(get_firestore_client)):
    try:
        # Weryfikacja roli admina
        if user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

        city_ref = db.collection("air_quality").document(location)
        history_docs = city_ref.collection("history").stream()

        for doc in history_docs:
            doc.reference.delete()

        city_ref.delete()

        return {"message": f"Flushed air quality data for {location}."}
    
    except Exception as e:
        logger.error(f"Error flushing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
