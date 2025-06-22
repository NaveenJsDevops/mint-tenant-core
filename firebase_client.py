import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Load env variables
load_dotenv()

# Load JSON from FIREBASE_CREDENTIALS env variable
firebase_creds_raw = os.environ.get("FIREBASE_CREDENTIALS")
if not firebase_creds_raw:
    raise RuntimeError("FIREBASE_CREDENTIALS not found in environment variables")

# Convert to dict and replace escaped newlines in private_key
cred_dict = json.loads(firebase_creds_raw)
cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Firestore & Auth
db = firestore.client()
firebase_auth = auth
