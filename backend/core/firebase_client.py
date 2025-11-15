import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import settings

# Get Firebase credentials from settings (environment variables)
firebase_creds_dict = settings.firebase_credentials_dict

# Create credentials from dictionary
cred = credentials.Certificate(firebase_creds_dict)

# Initialize Firebase Admin (only if not already initialized)
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized, which is fine
    pass

db = firestore.client()
