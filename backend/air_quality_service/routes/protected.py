from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from firebase_admin import auth
from ..auth import verify_firebase_token, admin_only
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/protected")
async def protected_route(user_data: dict = Depends(verify_firebase_token)):
    return {"message": "This is a protected API!", "user": user_data}

@router.get("/me")
@limiter.limit("/minute")
async def get_me(request: Request, response: Response, user=Depends(verify_firebase_token)):
    try:
        if not user or "uid" not in user:
            # Add cache headers to reduce retries
            response.headers["Cache-Control"] = "private, no-cache"
            raise HTTPException(
                status_code=401, 
                detail="Invalid Authorization"
            )
        
        # Add cache headers for successful responses
        response.headers["Cache-Control"] = "private, max-age=30"
        return user
        
    except HTTPException as e:
        # Return early with cache headers
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
            headers={"Cache-Control": "private, no-cache"}
        )

@router.get("/admin/users")
async def get_users(user=Depends(admin_only)):  # Use admin_only dependency
    try:
        # Pobieramy użytkowników z Firebase Authentication
        users = []
        page = auth.list_users()  # Pobierz pierwszą stronę użytkowników

        while page:
            for firebase_user in page.users:
                # Bezpiecznie sprawdzamy custom claims
                role = firebase_user.custom_claims.get("role") if firebase_user.custom_claims else "guest"
                
                # Zwracamy uid, email i role użytkowników
                users.append({
                    "uid": firebase_user.uid,
                    "email": firebase_user.email,
                    "role": role
                })
            
            # Jeśli jest kolejna strona, pobierz ją
            page = page.get_next_page()

        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")