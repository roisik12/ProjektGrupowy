from fastapi import APIRouter, HTTPException, Depends
from sklearn.linear_model import LinearRegression
import numpy as np
from .auth import verify_firebase_token as verify_token
import logging
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    history: list[float]

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict/{city}")
async def predict_aqi(
    city: str,
    request: PredictionRequest,
    current_user=Depends(verify_token)
):
    try:
        if len(request.history) < 5:
            raise HTTPException(
                status_code=400, 
                detail="Need at least 5 measurements for prediction"
            )

        # Prepare data for prediction - reverse to have oldest first
        history = request.history[:5][::-1]  # Get last 5 values and reverse
        values = np.array(history).reshape(-1, 1)
        time_points = np.array(range(len(values))).reshape(-1, 1)
        
        # Train simple linear model
        model = LinearRegression()
        model.fit(time_points, values)
        
        # Predict next value and ensure it's reasonable
        predicted = model.predict([[5]])[0]
        
        # Get min and max from history for bounds
        min_history = min(history)
        max_history = max(history)
        margin = (max_history - min_history) * 0.2  # Allow 20% deviation
        
        # Bound the prediction within reasonable limits
        predicted = max(min_history - margin, min(max_history + margin, predicted))
        predicted_aqi = round(float(predicted))
        
        # Ensure AQI is within valid range
        predicted_aqi = max(0, min(500, predicted_aqi))
        
        logger.debug(f"History: {history}, Predicted: {predicted_aqi}")
        
        return {
            "city": city,
            "predicted_aqi": predicted_aqi,
            "confidence": "low"
        }
    
    except Exception as e:
        logger.error(f"Prediction error for {city}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )