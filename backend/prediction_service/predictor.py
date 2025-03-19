import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import logging

logger = logging.getLogger(__name__)

def predict_aqi(data):
    """
    Predict the next day's AQI based on historical data.
    
    Parameters:
      data (list of dict): 
        Each dict must have 'AQI' (int) and 'last_update' (str in ISO format).
    
    Returns:
      float: Predicted AQI, clamped between 0 and 500.
    
    Raises:
      ValueError: If there are fewer than 5 valid data points.
    """
    logger.info(f"Starting AQI prediction. Number of raw records: {len(data)}")

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["last_update"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)
    df = df.drop_duplicates(subset=["timestamp"]).sort_values(by="timestamp")

    logger.info(f"After cleaning, we have {len(df)} records left for training.")

    if len(df) < 5:
        raise ValueError("Not enough data points to predict")
    df["seconds"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds()

    model = LinearRegression()
    X = df["seconds"].values.reshape(-1, 1)
    y = df["AQI"].values

    logger.info(f"Training LinearRegression with {len(X)} samples.")
    model.fit(X, y)

    future_time = np.array([[df["seconds"].max() + 86400]])
    predicted_aqi = model.predict(future_time)[0]

    predicted_aqi = max(0, min(500, predicted_aqi))
    return predicted_aqi
