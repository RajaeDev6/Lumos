from core.firebase_client import db
from utils.app_logger import logger

class RecommendationService:

    @staticmethod
    def save_recommendation(teacher_id: str, rec_id: str, rec_obj):
        try:
            db.collection("teachers").document(teacher_id)\
                .collection("recommendations").document(rec_id)\
                .set(rec_obj.to_dict(), merge=True)
        except Exception as e:
            logger.error(f"Error saving recommendation: {e}")

    @staticmethod
    def add_recommendation(teacher_id: str, rec_obj):
        """Add a recommendation with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("recommendations").document()
            doc_ref.set(rec_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding recommendation: {e}")
            return None

    @staticmethod
    def list_recommendations(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("recommendations").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing recommendations: {e}")
            return []

