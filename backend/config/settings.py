import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    PORT = os.getenv("PORT", 5000)
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

settings = Settings()
