import logging
from fastapi import APIRouter, HTTPException
from backend.prediction_service.database import get_history_data
from backend.prediction_service.predictor import predict_aqi
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
        data = get_history_data(location)

        logger.info(f"Raw data for {location}: {data}")

        if len(data) < 5:
            logger.warning(f"Not enough historical data for {location} to predict AQI")
            raise HTTPException(status_code=400, detail="Not enough historical data to predict")

        df = pd.DataFrame(data)

        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame head:\n{df.head(5).to_string(index=False)}")

        predicted_aqi = predict_aqi(data)

        logger.info(f"Predicted AQI for {location}: {predicted_aqi}")

        return {"location": location, "predicted_AQI": round(predicted_aqi, 2)}

    except HTTPException as e:
        raise e

    except ValueError as ve:
        logger.error(f"Prediction error for {location}: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Unexpected error in prediction for {location}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
