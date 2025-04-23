import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("backend/firebase_console_key.json")
firebase_admin.initialize_app(cred)

uid = "VWTXUkrf7JUprApOo2pPgCAZ1gG3"
auth.set_custom_user_claims(uid, {"role": "admin"})
print("Rola admin ustawiona!")