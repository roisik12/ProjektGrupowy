from fastapi import FastAPI
from .routes.prediction import router as prediction_router
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(prediction_router)

@app.get("/")
async def root():
    return {"message": "Prediction Service Running"}
