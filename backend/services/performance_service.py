from core.firebase_client import db
from utils.app_logger import logger

class PerformanceService:

    @staticmethod
    def save_overview(teacher_id: str, overview_obj):
        try:
            db.collection("teachers").document(teacher_id)\
                .collection("performance").document("overview")\
                .set(overview_obj.to_dict(), merge=True)
            return True
        except Exception as e:
            logger.error(f"Error saving performance overview: {e}")
            logger.exception("Full error details:")
            return False

    @staticmethod
    def get_overview(teacher_id: str):
        try:
            doc = db.collection("teachers").document(teacher_id)\
                   .collection("performance").document("overview").get()
            return doc.to_dict()
        except Exception as e:
            logger.error(f"Error fetching performance overview: {e}")
            return None

