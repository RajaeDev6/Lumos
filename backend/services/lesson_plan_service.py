from core.firebase_client import db
from utils.app_logger import logger

class LessonPlanService:

    @staticmethod
    def save_lesson_plan(teacher_id: str, plan_id: str, lesson_obj):
        try:
            db.collection("teachers").document(teacher_id)\
                .collection("lessonPlans").document(plan_id)\
                .set(lesson_obj.to_dict(), merge=True)
        except Exception as e:
            logger.error(f"Error saving lesson plan: {e}")

    @staticmethod
    def add_lesson_plan(teacher_id: str, lesson_obj):
        """Add a lesson plan with auto-generated ID and return the ID"""
        try:
            doc_ref = db.collection("teachers").document(teacher_id)\
                .collection("lessonPlans").document()
            doc_ref.set(lesson_obj.to_dict())
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error adding lesson plan: {e}")
            return None

    @staticmethod
    def list_lesson_plans(teacher_id: str):
        try:
            docs = db.collection("teachers").document(teacher_id)\
                    .collection("lessonPlans").stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error listing lesson plans: {e}")
            return []

