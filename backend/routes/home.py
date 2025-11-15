from flask import Blueprint, jsonify
from services.teacher_service import TeacherService
from models.teacher import Teacher
from utils.app_logger import logger

home = Blueprint("home", __name__)

@home.get("/")
def index():
    """Write and read from database, return JSON with status code"""
    try:
        teacher_id = "test_teacher_001"
        
        # Write to database
        logger.info("Writing teacher data to database...")
        teacher = Teacher(
            name="John Doe",
            email="john.doe@example.com",
            syllabus_status="uploaded",
            test_paper_status="uploaded",
            coverage=75,
            total_topics=10,
            weak_areas_count=2
        )
        
        write_success = TeacherService.save_teacher(teacher_id, teacher)
        
        if not write_success:
            return jsonify({
                "status": "error",
                "message": "Failed to write data to database. Please check Firebase connection."
            }), 500
        
        # Read from database
        logger.info("Reading teacher data from database...")
        teacher_data = TeacherService.get_teacher(teacher_id)
        
        if teacher_data:
            return jsonify({
                "status": "success",
                "message": "✓ Data successfully written to and retrieved from database!",
                "data": teacher_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Data was written but could not be retrieved from database."
            }), 500
            
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        logger.exception("Full error details:")
        return jsonify({
            "status": "error",
            "message": "An error occurred while processing the request",
            "error": str(e)
        }), 500
