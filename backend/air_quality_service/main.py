from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from backend.air_quality_service.routes import air_quality, protected

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Your API Title",
    description="API Description",
    version="1.0.0",
    docs_url="/docs",  # Explicitly set to /docs
    redoc_url=None,    # Disable redoc if not needed
    openapi_url="/openapi.json"  # Ensure this matches what Swagger UI expects
)

# Add limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Apply rate limiting to routes
@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Air Quality Service Running"}

# Include routers
app.include_router(air_quality.router)
app.include_router(protected.router)
