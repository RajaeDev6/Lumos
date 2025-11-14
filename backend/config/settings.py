import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    PORT = os.getenv("PORT", 5000)
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

settings = Settings()
