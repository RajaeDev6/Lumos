from core.firebase_client import db
from utils.app_logger import logger

class TeacherService:

    @staticmethod
    def get_teacher(teacher_id: str):
        try:
            doc = db.collection("teachers").document(teacher_id).get()
            return doc.to_dict()
        except Exception as e:
            logger.error(f"Error fetching teacher: {e}")
            return None

    @staticmethod
    def save_teacher(teacher_obj):
        """Save a teacher with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document()
            doc_ref.set(teacher_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error saving teacher: {e}")
            return None

    @staticmethod
    def update_field(teacher_id: str, field: str, value):
        try:
            db.collection("teachers").document(teacher_id).update({field: value})
        except Exception as e:
            logger.error(f"Error updating field: {e}")

