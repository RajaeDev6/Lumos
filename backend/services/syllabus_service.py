from core.firebase_client import db
from utils.app_logger import logger

class SyllabusService:

    @staticmethod
    def add_syllabus(teacher_id: str, syllabus_obj):
        """Add a syllabus with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("syllabi").document()
            doc_ref.set(syllabus_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding syllabus: {e}")
            return None

    @staticmethod
    def get_syllabus(teacher_id: str, syllabus_id: str):
        try:
            doc = db.collection("teachers").document(teacher_id)\
                   .collection("syllabi").document(syllabus_id).get()
            return doc.to_dict()
        except Exception as e:
            logger.error(f"Error fetching syllabus: {e}")
            return None

    @staticmethod
    def list_syllabi(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("syllabi").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing syllabi: {e}")
            return []

