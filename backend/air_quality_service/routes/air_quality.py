from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, UTC
import asyncio
import logging
from backend.air_quality_service.database import db, get_firestore_client
from backend.air_quality_service.models import AirQualityData, TrackedCity
from backend.air_quality_service.auth import admin_only, verify_firebase_token as verify_token
from backend.air_quality_service.weather_api import WeatherAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Initialize WeatherAPI
weather_api = WeatherAPI()

# Initialize scheduler as a singleton
_scheduler = None

def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler()
    return _scheduler

async def update_city_aqi(city: str, db=None):
    """Background task to update AQI data for a city"""
    try:
        logger.info(f"[UPDATE] Updating AQI data for {city}")
        
        if db is None:
            db = get_firestore_client()
            
        # Fetch new data from API
        weather_data = await weather_api.get_air_quality(city)
        if not weather_data:
            logger.error(f"[UPDATE] Failed to fetch new AQI data for {city}")
            return

        # Get reference to city's history collection
        city_ref = db.collection("air_quality").document(city)
        history_ref = city_ref.collection("history")
        
        # Get all records ordered by timestamp
        all_docs = list(history_ref.order_by("last_update", direction="DESCENDING").stream())
        
        if len(all_docs) >= 5:
            # Update the oldest record instead of creating a new one
            oldest_doc = all_docs[-1]  # Last document is the oldest
            oldest_doc.reference.set(weather_data)
            logger.info(f"[UPDATE] Updated oldest record for {city}")
        else:
            # If we have less than 5 records, create a new one
            new_doc = history_ref.document()
            new_doc.set(weather_data)
            logger.info(f"[UPDATE] Created new record for {city}")
        
        # Update city document
        city_ref.set({
            "name": city,
            "last_update": weather_data["last_update"]
        }, merge=True)
                
        logger.info(f"[UPDATE] Successfully updated AQI data for {city}")
        
    except Exception as e:
        logger.error(f"[UPDATE] Error updating AQI for {city}: {e}")

async def update_all_cities():
    """Update AQI data for all cities in the database"""
    try:
        db = get_firestore_client()
        cities = db.collection("air_quality").stream()
        
        # Get unique city names
        city_names = set(city.id for city in cities)
        
        # Update each city
        for city in city_names:
            await update_city_aqi(city, db)
            
    except Exception as e:
        logger.error(f"[UPDATE] Error in update_all_cities: {e}")

# Start the scheduler when the application starts
@router.on_event("startup")
async def start_scheduler():
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.add_job(update_all_cities, 'interval', hours=6)
        scheduler.start()
        logger.info("Scheduler started successfully")

# Stop the scheduler when the application shuts down
@router.on_event("shutdown")
async def stop_scheduler():
    scheduler = get_scheduler()
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully")

@router.post("/user/tracked-cities/{city}")
@limiter.limit("5/minute")
async def track_city(request: Request, city: str, user=Depends(verify_token), db=Depends(get_firestore_client)):
    try:
        logger.info(f"[TRACK] Starting track_city for {city}")
        logger.info(f"[TRACK] User {user['email']} is tracking city {city}")
        
        # First check if the city exists by trying to get its data
        try:
            logger.info(f"[TRACK] Calling get_air_quality for {city}")
            result = await get_air_quality(request, city, db)
            logger.info(f"[TRACK] get_air_quality returned data for {city}: {result is not None}")
        except HTTPException as he:
            logger.error(f"[TRACK] get_air_quality failed for {city}: {he.detail}")
            raise he
        
        # If we get here, the city exists and has data
        # Add to user's tracked cities
        user_ref = db.collection("user_preferences").document(user["uid"])
        doc = user_ref.get()
        tracked_cities = []
        if doc.exists:
            tracked_cities = doc.to_dict().get("tracked_cities", [])
            if any(tc.get("city") == city for tc in tracked_cities):
                return {"message": f"City {city} is already being tracked"}
        
        # Add new city to tracked cities
        tracked_city = TrackedCity(city=city).model_dump()
        tracked_cities.append(tracked_city)
        user_ref.set({"tracked_cities": tracked_cities}, merge=True)

        return {"message": f"Now tracking {city}"}
        
    except Exception as e:
        logger.error(f"Error tracking city: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/air-quality/{location}")
@limiter.limit("10/minute")
async def get_air_quality(request: Request, location: str, db=Depends(get_firestore_client)):
    """Return AQI data from Firestore, fetch from Open-Meteo if none exists"""
    try:
        logger.info(f"[AQI] Starting get_air_quality for {location}")
        
        # Get reference to city's history collection
        city_ref = db.collection("air_quality").document(location)
        history_ref = city_ref.collection("history")
        
        # Get only 5 most recent documents
        docs = list(history_ref.order_by("last_update", direction="DESCENDING")
                   .limit(5)
                   .stream())
        
        logger.info(f"[AQI] Found {len(docs)} existing records for {location}")
        
        # If no data exists, fetch from Open-Meteo
        if not docs:
            logger.info(f"No data found for {location}, fetching from Open-Meteo")
            weather_data = await weather_api.get_air_quality(location)
            
            if not weather_data:
                raise HTTPException(status_code=404, detail=f"City {location} not found")
            
            # Save the data
            city_ref.set({
                "name": location,
                "last_update": weather_data["last_update"]
            }, merge=True)
            
            new_doc = history_ref.document()
            new_doc.set(weather_data)
            
            logger.info(f"Saved new AQI data for {location}")
            
            return {"location": location, "history": [weather_data]}
        
        # Return existing data
        data = [doc.to_dict() for doc in docs]
        logger.info(f"Found {len(data)} records for {location}")
        
        return {"location": location, "history": data}

    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST request: Zapis danych o jakości powietrza
@router.post("/air-quality/{location}")
@limiter.limit("5/minute")
async def set_air_quality(request: Request, location: str, data: AirQualityData, user=Depends(admin_only), db=Depends(get_firestore_client)):
    try:
        logger.info(f"[{user['email']}] is saving AQI data for {location}")
        logger.info(f"Saving air quality data for {location}")

        city_ref = db.collection("air_quality").document(location)
        
        # Get the history collection reference
        history_ref = city_ref.collection("history")
        
        # Get all documents ordered by timestamp
        docs = history_ref.order_by("last_update", direction="DESCENDING").limit(10).stream()
        existing_docs = list(docs)
        
        # Add new document
        new_doc = history_ref.document()
        new_doc.set({
            "AQI": data.AQI,
            "last_update": data.last_update
        })
        
        # If we have more than 10 documents after adding the new one,
        # delete the oldest ones
        if len(existing_docs) >= 10:
            # Get the oldest documents (all after the first 9)
            docs_to_delete = existing_docs[9:]
            for doc in docs_to_delete:
                doc.reference.delete()

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

@router.post("/user/tracked-cities/{city}")
@limiter.limit("5/minute")
async def track_city(request: Request, city: str, user=Depends(verify_token), db=Depends(get_firestore_client)):
    try:
        logger.info(f"[TRACK] Starting track_city for {city}")
        logger.info(f"[TRACK] User {user['email']} is tracking city {city}")
        
        # 1. Check and fetch AQI data
        city_ref = db.collection("air_quality").document(city)
        history_ref = city_ref.collection("history")
        
        # Get existing data
        existing_data = list(history_ref.order_by("last_update", direction="DESCENDING").limit(1).stream())

        # Always fetch fresh data when tracking a new city
        logger.info(f"Fetching fresh data for {city}")
        weather_data = await weather_api.get_air_quality(city)
        
        if not weather_data:
            raise HTTPException(status_code=404, detail=f"City {city} not found")
            
        # Save new AQI data and ensure we keep only 10 most recent readings
        new_doc = history_ref.document()
        new_doc.set(weather_data)
        logger.info(f"Saved new AQI data for {city}: {weather_data}")
        
        # Cleanup old data if we have more than 10 entries
        all_docs = list(history_ref.order_by("last_update", direction="DESCENDING").stream())
        if len(all_docs) > 10:
            for old_doc in all_docs[10:]:
                old_doc.reference.delete()
                logger.info(f"Deleted old AQI data for {city}")
        
        # 2. Add to user's tracked cities
        user_ref = db.collection("user_preferences").document(user["uid"])
        doc = user_ref.get()
        tracked_cities = []
        if doc.exists:
            tracked_cities = doc.to_dict().get("tracked_cities", [])
            if any(tc.get("city") == city for tc in tracked_cities):
                return {"message": f"City {city} is already being tracked"}
        
        # Add new city to tracked cities
        tracked_city = TrackedCity(city=city).model_dump()
        tracked_cities.append(tracked_city)
        user_ref.set({"tracked_cities": tracked_cities}, merge=True)

        # 3. Return both tracking confirmation and current AQI data
        latest_data = await get_air_quality(request, city, db)
        return {
            "message": f"Now tracking {city}",
            "current_data": latest_data
        }
        
    except Exception as e:
        logger.error(f"Error tracking city: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/tracked-cities")
@limiter.limit("10/minute")
async def get_tracked_cities(
    request: Request,
    user=Depends(verify_token),
    db=Depends(get_firestore_client)
):
    try:
        logger.info(f"Fetching tracked cities for user {user['email']}")
        
        # Get user's preferences document
        doc = db.collection("user_preferences").document(user["uid"]).get()
        
        if not doc.exists:
            return {"tracked_cities": []}
            
        user_data = doc.to_dict()
        tracked_cities = user_data.get("tracked_cities", [])
        
        # For each tracked city, get the AQI data using get_air_quality
        result = []
        for city_data in tracked_cities:
            city = city_data["city"]
            try:
                aqi_data = await get_air_quality(request, city, db)
                result.append({
                    **city_data,
                    "history": aqi_data["history"]
                })
            except HTTPException:
                # If no data found, skip this city
                logger.warning(f"No AQI data found for tracked city: {city}")
                result.append({
                    **city_data,
                    "history": []
                })
            
        return {"tracked_cities": result}
        
    except Exception as e:
        logger.error(f"Error fetching tracked cities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user/tracked-cities/{city}")
@limiter.limit("5/minute")
async def untrack_city(
    request: Request,
    city: str,
    user=Depends(verify_token),
    db=Depends(get_firestore_client)
):
    try:
        logger.info(f"User {user['email']} is untracking city {city}")
        
        # Reference to user's preferences document
        user_ref = db.collection("user_preferences").document(user["uid"])
        
        # Get current tracked cities
        doc = user_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="No tracked cities found")
            
        tracked_cities = doc.to_dict().get("tracked_cities", [])
        
        # Remove the city
        tracked_cities = [tc for tc in tracked_cities if tc.get("city") != city]
        
        # Update Firestore
        user_ref.set({"tracked_cities": tracked_cities}, merge=True)
        
        return {"message": f"Stopped tracking {city}"}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error untracking city: {e}")
        raise HTTPException(status_code=500, detail=str(e))
