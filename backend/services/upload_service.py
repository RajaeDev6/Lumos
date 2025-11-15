from core.firebase_client import db
from utils.app_logger import logger

class UploadService:

    @staticmethod
    def record_upload(teacher_id: str, upload_id: str, upload_obj):
        try:
            db.collection("teachers").document(teacher_id)\
                .collection("uploads").document(upload_id)\
                .set(upload_obj.to_dict(), merge=True)
        except Exception as e:
            logger.error(f"Error recording upload: {e}")

    @staticmethod
    def add_upload(teacher_id: str, upload_obj):
        """Add an upload record with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("uploads").document()
            doc_ref.set(upload_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding upload: {e}")
            return None

    @staticmethod
    def list_uploads(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("uploads").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing uploads: {e}")
            return []

