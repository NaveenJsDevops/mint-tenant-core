import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Load environment variables from .env (for local development)
load_dotenv()

# Load credentials from FIREBASE_CREDENTIALS environment variable
firebase_creds_raw = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_creds_raw:
    raise RuntimeError("FIREBASE_CREDENTIALS not found in environment variables.")

try:
    cred_dict = json.loads(firebase_creds_raw)
except json.JSONDecodeError as e:
    raise ValueError("Invalid JSON in FIREBASE_CREDENTIALS") from e

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Initialize Firestore and Auth clients
db = firestore.client()
firebase_auth = auth
