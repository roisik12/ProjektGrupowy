from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import auth
from ..auth import verify_firebase_token
router = APIRouter()

@router.get("/protected")
async def protected_route(user_data: dict = Depends(verify_firebase_token)):
    return {"message": "This is a protected API!", "user": user_data}

@router.get("/me")
def get_me(user=Depends(verify_firebase_token)):
    if not user or "uid" not in user:  # Zamiast "user_id" używamy "uid"
        raise HTTPException(status_code=401, detail="Błąd autoryzacji: brak user_id")

    return user
@router.get("/admin/users")
async def get_users(user=Depends(verify_firebase_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

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