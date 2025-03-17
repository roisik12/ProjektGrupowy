import logging
from fastapi import APIRouter, HTTPException
from ..database import get_history_data
from ..predictor import predict_aqi
import pandas as pd

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/predict/{location}")
async def predict_air_quality(location: str):
    """
    Fetch historical data for 'location' and return predicted AQI for the next day.
    Logs additional info about the data used for the prediction.
    """
    try:
        # Fetch data from Firestore
        data = get_history_data(location)

        # Log the raw data for debugging
        logger.info(f"Raw data for {location}: {data}")

        if len(data) < 5:
            logger.warning(f"Not enough historical data for {location} to predict AQI")
            raise HTTPException(status_code=400, detail="Not enough historical data to predict")

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Log shape and head of the DataFrame
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame head:\n{df.head(5).to_string(index=False)}")

        # Run the ML model to predict AQI
        predicted_aqi = predict_aqi(data)

        # Log the final prediction
        logger.info(f"Predicted AQI for {location}: {predicted_aqi}")

        return {"location": location, "predicted_AQI": round(predicted_aqi, 2)}

    except HTTPException as e:
        # Pass along HTTPExceptions as they are
        raise e

    except ValueError as ve:
        # e.g., If predict_aqi raises "Not enough data points"
        logger.error(f"Prediction error for {location}: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Unexpected error in prediction for {location}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
