from fastapi import FastAPI
from .routes import air_quality, protected

app = FastAPI()

app.include_router(air_quality.router)
app.include_router(protected.router)

@app.get("/")
async def root():
    return {"message": "Air Quality Service Running"}
