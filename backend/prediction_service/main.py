from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import numpy as np
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
# Get the absolute path of firestore_key.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../../firestore_key.json")

# Set Firestore authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# Initialize FastAPI
app = FastAPI()

# Initialize Firestore
db = firestore.Client()

@app.get("/")
async def root():
    return {"message": "Prediction Service Running"}

@app.get("/predict/{location}")
async def predict_air_quality(location: str):
    try:
        logger.info(f"📡 Fetching historical AQI data for prediction: {location}")
        
        # Fetch historical data from Firestore
        docs = db.collection("air_quality").document(location).collection("history").stream()
        data = []
        
        for doc in docs:
            entry = doc.to_dict()
            if "AQI" in entry and "last_update" in entry:
                data.append(entry)  # ✅ Store full dict to avoid re-processing later

        # Ensure at least 5 data points for a meaningful prediction
        if len(data) < 5:
            logger.warning(f"⚠️ Not enough historical data for {location} to predict AQI")
            raise HTTPException(status_code=400, detail="Not enough historical data to predict")

        # ✅ Fix: Use `last_update` correctly, ignoring Firestore timestamps
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["last_update"], errors="coerce")  # ✅ Convert properly
        df.dropna(inplace=True)  # Remove invalid timestamps
        df = df.drop_duplicates(subset=["timestamp"]).sort_values(by="timestamp")  # ✅ Ensure unique and sorted data

        # 🔥 Log dataset for debugging
        logger.info("\n==== TRAINING DATA USED FOR PREDICTION ====")
        logger.info(df.to_string(index=False))

        # Train a Linear Regression model
        model = LinearRegression()
        X = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds().values.reshape(-1, 1)  # ✅ Normalize time
        y = df["AQI"].values
        model.fit(X, y)

        # Predict AQI for the next day (+1 day = 86400 seconds)
        future_time = np.array([[X.max() + 86400]])  
        predicted_aqi = model.predict(future_time)[0]

        # Ensure the predicted AQI stays within valid bounds (0-500)
        predicted_aqi = max(0, min(500, predicted_aqi))

        # 🔥 Log predicted AQI
        logger.info(f"📊 Prediction for {location} - Predicted AQI: {round(predicted_aqi, 2)}")

        return {"location": location, "predicted_AQI": round(predicted_aqi, 2)}
    
    except HTTPException as e:
        raise e  # ✅ Keep the correct error code

    except Exception as e:
        logger.error(f"❌ Unexpected error in prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")  # ✅ Only trigger 500 for real issues