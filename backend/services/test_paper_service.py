from core.firebase_client import db
from utils.app_logger import logger

class TestPaperService:

    @staticmethod
    def add_test_paper(teacher_id: str, test_obj):
        """Add a test paper with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("testPapers").document()
            doc_ref.set(test_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding test paper: {e}")
            return None

    @staticmethod
    def list_test_papers(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("testPapers").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing test papers: {e}")
            return []

