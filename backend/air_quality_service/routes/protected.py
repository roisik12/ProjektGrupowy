from fastapi import APIRouter, Depends
from ..auth import verify_firebase_token

router = APIRouter()

@router.get("/protected")
async def protected_route(user_data: dict = Depends(verify_firebase_token)):
    return {"message": "This is a protected API!", "user": user_data}