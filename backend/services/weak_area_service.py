from core.firebase_client import db
from utils.app_logger import logger

class WeakAreaService:

    @staticmethod
    def save_weak_area(teacher_id: str, topic_id: str, weak_obj):
        try:
            db.collection("teachers").document(teacher_id)\
                .collection("weakAreas").document(topic_id)\
                .set(weak_obj.to_dict(), merge=True)
        except Exception as e:
            logger.error(f"Error saving weak area: {e}")

    @staticmethod
    def add_weak_area(teacher_id: str, weak_obj):
        """Add a weak area with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("weakAreas").document()
            doc_ref.set(weak_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding weak area: {e}")
            return None

    @staticmethod
    def list_weak_areas(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("weakAreas").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing weak areas: {e}")
            return []

