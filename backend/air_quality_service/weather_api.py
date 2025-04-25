import httpx
import logging
from datetime import datetime, UTC

logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self):
        self.base_url = "https://air-quality-api.open-meteo.com/v1"
    
    async def get_air_quality(self, city: str) -> dict:
        """Fetch air quality data for a city using Open-Meteo"""
        try:
            # First get coordinates for the city using Open-Meteo Geocoding API
            async with httpx.AsyncClient() as client:
                logger.info(f"Fetching coordinates for {city}")
                geo_response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "name": city,
                        "count": 1,
                        "language": "en",
                        "format": "json"
                    }
                )
                geo_data = geo_response.json()
                
                if not geo_data.get("results"):
                    logger.error(f"City not found: {city}")
                    return None
                
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                
                logger.info(f"Found coordinates for {city}: lat={lat}, lon={lon}")
                
                # Then get air quality data
                aqi_response = await client.get(
                    f"{self.base_url}/air-quality",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": ["european_aqi", "us_aqi", "pm2_5", "pm10"],
                        "domains": "cams_europe"
                    }
                )
                
                if not aqi_response.is_success:
                    logger.error(f"Failed to fetch AQI data: {aqi_response.text}")
                    return None
                
                aqi_data = aqi_response.json()
                
                # Get both European and US AQI
                eu_aqi = aqi_data["current"]["european_aqi"]
                us_aqi = aqi_data["current"]["us_aqi"]
                pm2_5 = aqi_data["current"]["pm2_5"]
                pm10 = aqi_data["current"]["pm10"]
                
                return {
                    "AQI": us_aqi,  # Using US AQI directly instead of conversion
                    "last_update": datetime.now(UTC).isoformat(),
                    "source": "Open-Meteo",
                    "raw_data": {
                        "european_aqi": eu_aqi,
                        "us_aqi": us_aqi,
                        "pm2_5": pm2_5,
                        "pm10": pm10,
                        "latitude": lat,
                        "longitude": lon
                    }
                }
                
        except Exception as e:
            logger.error(f"Error fetching air quality data: {e}")
            return None