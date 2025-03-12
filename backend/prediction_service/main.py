from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import numpy as np
import logging
import pandas as pd
from sklearn.linear_model import LinearRegression

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
        logger.info(f"Fetching historical AQI data for prediction: {location}")
        
        # Fetch historical data from Firestore
        docs = db.collection("air_quality").document(location).collection("history").stream()
        data = []
        
        for doc in docs:
            entry = doc.to_dict()
            if "AQI" in entry and "last_update" in entry:
                data.append((entry["last_update"], entry["AQI"]))

        # Ensure at least 5 data points for a meaningful prediction
        if len(data) < 5:
            raise HTTPException(status_code=400, detail="Not enough historical data to predict")

        # Convert data into a Pandas DataFrame and sort it by date
        df = pd.DataFrame(data, columns=["last_update", "AQI"])
        df["timestamp"] = pd.to_datetime(df["last_update"]).astype(np.int64) // 10**9  # Convert to Unix timestamp
        df = df.sort_values(by="timestamp")  # Ensure chronological order

        # Log the dataset for debugging
        logger.info(f"Training data for {location}:\n{df}")

        # Train a Linear Regression model
        model = LinearRegression()
        X = df["timestamp"].values.reshape(-1, 1)
        y = df["AQI"].values
        model.fit(X, y)

        # Predict AQI for the next day (+1 day = 86400 seconds)
        future_time = np.array([[df["timestamp"].max() + 86400]])  
        predicted_aqi = model.predict(future_time)[0]

        # Ensure the predicted AQI stays within valid bounds (0-500)
        predicted_aqi = max(0, min(500, predicted_aqi))

        return {"location": location, "predicted_AQI": round(predicted_aqi, 2)}
    
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
