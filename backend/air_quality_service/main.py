from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import air_quality, protected

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow GET, POST, OPTIONS, DELETE, etc.
    allow_headers=["*"],  # ✅ Allow all headers, including Authorization
)
app.include_router(air_quality.router)
app.include_router(protected.router)

@app.get("/")
async def root():
    return {"message": "Air Quality Service Running"}
