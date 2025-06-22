import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Load env variables from .env
load_dotenv()

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not FIREBASE_CREDENTIALS_PATH:
    raise RuntimeError("FIREBASE_CREDENTIALS_PATH not set in .env")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
firebase_auth = auth
