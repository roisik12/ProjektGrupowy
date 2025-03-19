import firebase_admin
from firebase_admin import credentials, auth
import os
import json
import httpx

# Pobierz ścieżkę do klucza Firebase
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "../firebase_config.json")
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "../backend/firebase_console_key.json")

# Inicjalizacja Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

def get_firebase_api_key():
    """Load Firebase API Key from JSON config file."""
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config = json.load(config_file)
            return config.get("apiKey", None)
    except FileNotFoundError:
        raise RuntimeError("🔥 firebase_config.json not found! Ensure the file exists in the root directory.")

FIREBASE_API_KEY = get_firebase_api_key()
    
def get_firebase_token(email: str, password: str):
    """Tworzy testowego użytkownika, loguje go i zwraca poprawny Firebase ID Token"""
    
    try:
        # Sprawdź, czy użytkownik już istnieje
        user = auth.get_user_by_email(email)
    except:
        # Jeśli nie istnieje, utwórz użytkownika
        user = auth.create_user(email=email, password=password)

    # Generowanie custom tokena
    custom_token = auth.create_custom_token(user.uid).decode("utf-8")

    # Wymiana custom tokena na ID token (za pomocą Firebase Auth API)
    response = httpx.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={FIREBASE_API_KEY}",
        json={"token": custom_token, "returnSecureToken": True},
    )

    if response.status_code == 200:
        return response.json()["idToken"]  # ✅ Teraz zwracamy poprawny ID Token
    else:
        raise ValueError(f"Firebase auth failed: {response.json()}")
