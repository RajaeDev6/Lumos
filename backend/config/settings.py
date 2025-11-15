import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    PORT = os.getenv("PORT", 5000)
    
    # Firebase Admin credentials (individual fields from env)
    FIREBASE_TYPE = os.getenv("FIREBASE_TYPE", "service_account")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID = os.getenv("FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")
    FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID = os.getenv("FIREBASE_CLIENT_ID")
    FIREBASE_AUTH_URI = os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
    FIREBASE_TOKEN_URI = os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token")
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs")
    FIREBASE_CLIENT_X509_CERT_URL = os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    FIREBASE_UNIVERSE_DOMAIN = os.getenv("FIREBASE_UNIVERSE_DOMAIN", "googleapis.com")
    
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    @property
    def firebase_credentials_dict(self):
        """Build Firebase credentials dictionary from environment variables"""
        return {
            "type": self.FIREBASE_TYPE,
            "project_id": self.FIREBASE_PROJECT_ID,
            "private_key_id": self.FIREBASE_PRIVATE_KEY_ID,
            "private_key": self.FIREBASE_PRIVATE_KEY,
            "client_email": self.FIREBASE_CLIENT_EMAIL,
            "client_id": self.FIREBASE_CLIENT_ID,
            "auth_uri": self.FIREBASE_AUTH_URI,
            "token_uri": self.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": self.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": self.FIREBASE_CLIENT_X509_CERT_URL,
            "universe_domain": self.FIREBASE_UNIVERSE_DOMAIN
        }

settings = Settings()
