from firebase_admin import credentials, firestore
from config.settings import settings

firebase_creds = settings.FIREBASE_CREDENTIALS

cred = credentials.Certificate(firebase_creds)

firebase_admin.initialize_app(cred)

db = firestore.client()
