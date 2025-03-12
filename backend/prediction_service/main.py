from fastapi import FastAPI, HTTPException
from google.cloud import firestore
import os
import numpy as np
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
        # Fetch historical data from Firestore's "history" subcollection
        docs = db.collection("air_quality").document(location).collection("history").stream()
        data = []
        
        for doc in docs:
            entry = doc.to_dict()
            if "AQI" in entry and "last_update" in entry:
                data.append((entry["last_update"], entry["AQI"]))

        # Ensure we have at least 5 data points
        if len(data) < 5:
            raise HTTPException(status_code=400, detail="Not enough historical data to predict")

        # Convert data into a Pandas DataFrame
        df = pd.DataFrame(data, columns=["last_update", "AQI"])
        df["timestamp"] = pd.to_datetime(df["last_update"]).astype(int) // 10**9  # Convert to Unix timestamp

        # Print the dataset for debugging
        print("\n==== DATASET USED FOR PREDICTION ====")
        print(df)

        # Train a Linear Regression model
        model = LinearRegression()
        X = df["timestamp"].values.reshape(-1, 1)
        y = df["AQI"].values
        model.fit(X, y)

        # Predict AQI for the next day
        future_time = np.array([[df["timestamp"].max() + 86400]])  # +1 day
        predicted_aqi = model.predict(future_time)[0]

        return {"location": location, "predicted_AQI": round(predicted_aqi, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
