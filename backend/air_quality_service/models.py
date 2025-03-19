from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC
from typing import Optional

class AirQualityData(BaseModel):
    AQI: int = Field(..., ge=0, le=500, description="Air Quality Index must be between 0 and 500")
    last_update: Optional[str] = None

    @field_validator("last_update", mode="before")
    @classmethod
    def set_last_update(cls, value):
        """Ensure `last_update` is correctly formatted or set to the current UTC time."""
        if not value:
            return datetime.now(UTC).isoformat()  # ✅ Use timezone-aware datetime
        return value