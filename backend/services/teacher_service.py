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
    def save_teacher(teacher_id: str, teacher_obj):
        try:
            db.collection("teachers").document(teacher_id).set(
                teacher_obj.to_dict(), merge=True
            )
            return True
        except Exception as e:
            logger.error(f"Error saving teacher: {e}")
            return False

    @staticmethod
    def update_field(teacher_id: str, field: str, value):
        try:
            db.collection("teachers").document(teacher_id).update({field: value})
        except Exception as e:
            logger.error(f"Error updating field: {e}")

