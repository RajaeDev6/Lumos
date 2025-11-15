import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import settings

firebase_creds = settings.FIREBASE_CREDENTIALS

cred = credentials.Certificate(firebase_creds)

# Initialize Firebase Admin (only if not already initialized)
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized, which is fine
    pass

db = firestore.client()
