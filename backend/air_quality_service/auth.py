import os
import logging
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header, Depends

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "../firebase_console_key.json")
USING_EMULATOR = "FIREBASE_AUTH_EMULATOR_HOST" in os.environ

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

def verify_firebase_token(authorization: str = Header(None)):
    """Verify Firebase ID token and return decoded user info"""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")

    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        logger.info(f"Decoded Token: {decoded_token}")

        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "role": decoded_token.get("role", "guest"),  # <---- KLUCZOWE
            "token": token
        }
    except Exception as e:
        logger.error(f"Token Verification Error: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {e}")
def admin_only(user=Depends(verify_firebase_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user