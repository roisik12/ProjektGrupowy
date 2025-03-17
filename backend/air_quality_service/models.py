from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class AirQualityData(BaseModel):
    AQI: int = Field(..., ge=0, le=500, description="Air Quality Index must be between 0 and 500")
    last_update: Optional[str] = None

    @validator("last_update", pre=True, always=True)
    def set_last_update(cls, value):
        if not value:
            return datetime.utcnow().isoformat()
        return value
