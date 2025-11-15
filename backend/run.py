"""
Firebase Connection Test Script
This script tests Firebase Firestore connection by:
1. Writing sample data to the database
2. Reading the data back to verify the connection
"""
from models.teacher import Teacher
from models.syllabus import Syllabus
from models.test_paper import TestPaper
from models.weak_area import WeakArea
from models.recommendation import Recommendation
from models.upload_record import UploadRecord
from models.lesson_plan import LessonPlan
from models.performance_overview import PerformanceOverview

from services.teacher_service import TeacherService
from services.syllabus_service import SyllabusService
from services.test_paper_service import TestPaperService
from services.weak_area_service import WeakAreaService
from services.recommendation_service import RecommendationService
from services.upload_service import UploadService
from services.lesson_plan_service import LessonPlanService
from services.performance_service import PerformanceService
from services.storage_service import StorageService

from datetime import datetime
from utils.app_logger import logger
import json
import os

def upload_files_from_backend_root(teacher_id: str):
    """Upload PDF and Word documents from backend root to Cloudinary"""
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 0: UPLOADING FILES TO CLOUDINARY")
    logger.info("=" * 60)
    
    try:
        # Get backend root (same directory as run.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Supported document file extensions
        doc_extensions = ['.pdf', '.doc', '.docx']
        found_files = []
        
        # Look for document files in backend root
        for file in os.listdir(current_dir):
            file_path = os.path.join(current_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file.lower())
                if ext in doc_extensions:
                    found_files.append(file_path)
        
        if not found_files:
            logger.warning(f"⚠ No document files found in backend root")
            logger.info(f"  Searched in: {current_dir}")
            logger.info(f"  Looking for: {', '.join(doc_extensions)}")
            logger.info("=" * 60)
            return {}
        
        logger.info(f"Found {len(found_files)} document file(s):")
        for file_path in found_files:
            logger.info(f"  - {os.path.basename(file_path)}")
        
        # Upload folder
        folder = f"teachers/{teacher_id}/documents"
        
        # If single file, use single upload
        if len(found_files) == 1:
            logger.info(f"\nUploading single file to Cloudinary...")
            logger.info(f"  Folder: {folder}")
            
            file_path = found_files[0]
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            public_id = f"{filename_without_ext}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            url = StorageService.upload_file(
                file_path=file_path,
                folder=folder,
                public_id=public_id,
                resource_type="raw"
            )
            
            if url:
                logger.info("=" * 60)
                logger.info("✓ SUCCESS: File uploaded to Cloudinary!")
                logger.info(f"  File: {filename}")
                logger.info(f"  Download URL: {url}")
                logger.info("=" * 60)
                return {file_path: url}
            else:
                logger.error("=" * 60)
                logger.error("✗ FAILED: File upload to Cloudinary failed")
                logger.error("  Check Cloudinary credentials and connection")
                logger.info("=" * 60)
                return {file_path: None}
        
        # If multiple files, use bulk upload
        else:
            logger.info(f"\nUploading {len(found_files)} files in bulk to Cloudinary...")
            logger.info(f"  Folder: {folder}")
            
            results = StorageService.upload_files_bulk(
                file_paths=found_files,
                folder=folder,
                resource_type="raw"
            )
            
            successful = sum(1 for url in results.values() if url is not None)
            failed = len(results) - successful
            
            logger.info("=" * 60)
            if successful > 0:
                logger.info(f"✓ SUCCESS: {successful} file(s) uploaded successfully!")
                for file_path, url in results.items():
                    if url:
                        logger.info(f"  ✓ {os.path.basename(file_path)}: {url}")
            if failed > 0:
                logger.error(f"✗ FAILED: {failed} file(s) failed to upload")
                for file_path, url in results.items():
                    if url is None:
                        logger.error(f"  ✗ {os.path.basename(file_path)}")
            logger.info("=" * 60)
            
            return results
            
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"✗ ERROR: Exception occurred during file upload")
        logger.error(f"  Error: {str(e)}")
        logger.exception("Full error details:")
        logger.info("=" * 60)
        return {}

def write_data_to_firebase(teacher_id: str):
    """Write sample data to Firebase Firestore"""
    logger.info("=" * 60)
    logger.info("PHASE 1: WRITING DATA TO FIREBASE")
    logger.info("=" * 60)
    
    saved_ids = {}
    
    try:
        # 1. Teacher
        logger.info("\n[1/8] Saving Teacher...")
        teacher = Teacher(
            name="John Brown",
            email="john.brown@example.com",
            syllabus_status="uploaded",
            test_paper_status="uploaded",
            coverage=72,
            total_topics=14,
            weak_areas_count=3
        )
        TeacherService.save_teacher(teacher_id, teacher)
        logger.info(f"✓ Teacher saved successfully")
        saved_ids['teacher'] = teacher_id

        # 2. Syllabus
        logger.info("\n[2/8] Saving Syllabus...")
        syllabus = Syllabus(
            file_name="syllabus.pdf",
            file_url="https://url/syllabus.pdf",
            extracted_topics=[{"topicName": "Quadratic Equations"}],
            status="processed",
            academic_year="2024",
            upload_date=str(datetime.now())
        )
        syllabus_id = SyllabusService.add_syllabus(teacher_id, syllabus)
        if syllabus_id:
            logger.info(f"✓ Syllabus saved with ID: {syllabus_id}")
            saved_ids['syllabus'] = syllabus_id
        else:
            logger.error("✗ Failed to save syllabus")

        # 3. Test Paper
        logger.info("\n[3/8] Saving Test Paper...")
        test_paper = TestPaper(
            file_name="test.pdf",
            file_url="https://url/test.pdf",
            status="processed",
            upload_date=str(datetime.now())
        )
        test_paper_id = TestPaperService.add_test_paper(teacher_id, test_paper)
        if test_paper_id:
            logger.info(f"✓ Test Paper saved with ID: {test_paper_id}")
            saved_ids['test_paper'] = test_paper_id
        else:
            logger.error("✗ Failed to save test paper")

        # 4. Weak Area
        logger.info("\n[4/8] Saving Weak Area...")
        weak_area = WeakArea(
            topic_name="Quadratic Equations",
            mastery=42,
            difficulty="High",
            last_updated=str(datetime.now())
        )
        weak_area_id = WeakAreaService.add_weak_area(teacher_id, weak_area)
        if weak_area_id:
            logger.info(f"✓ Weak Area saved with ID: {weak_area_id}")
            saved_ids['weak_area'] = weak_area_id
        else:
            logger.error("✗ Failed to save weak area")

        # 5. Recommendation
        logger.info("\n[5/8] Saving Recommendation...")
        rec = Recommendation(
            index=1,
            recommendation="Practice quadratics",
            topic="Quadratic Equations",
            created_at=str(datetime.now())
        )
        rec_id = RecommendationService.add_recommendation(teacher_id, rec)
        if rec_id:
            logger.info(f"✓ Recommendation saved with ID: {rec_id}")
            saved_ids['recommendation'] = rec_id
        else:
            logger.error("✗ Failed to save recommendation")

        # 6. Upload
        logger.info("\n[6/8] Saving Upload Record...")
        upload = UploadRecord(
            file_name="test.pdf",
            file_type="testPaper",
            file_url="https://url/test.pdf",
            upload_date=str(datetime.now())
        )
        upload_id = UploadService.add_upload(teacher_id, upload)
        if upload_id:
            logger.info(f"✓ Upload saved with ID: {upload_id}")
            saved_ids['upload'] = upload_id
        else:
            logger.error("✗ Failed to save upload")

        # 7. Lesson Plan
        logger.info("\n[7/8] Saving Lesson Plan...")
        lesson = LessonPlan(
            topic="Quadratics",
            objectives=["Solve quadratics"],
            activities=["Examples"],
            assessments=["Quiz"],
            created_at=str(datetime.now())
        )
        lesson_id = LessonPlanService.add_lesson_plan(teacher_id, lesson)
        if lesson_id:
            logger.info(f"✓ Lesson Plan saved with ID: {lesson_id}")
            saved_ids['lesson_plan'] = lesson_id
        else:
            logger.error("✗ Failed to save lesson plan")

        # 8. Performance Overview
        logger.info("\n[8/8] Saving Performance Overview...")
        perf = PerformanceOverview(
            coverage=72,
            syllabus_uploaded=True,
            test_papers_uploaded=True,  # Fixed: was test_paper_uploaded (singular)
            weak_areas_count=3,
            recommendations_count=1,
            last_updated=str(datetime.now())
        )
        success = PerformanceService.save_overview(teacher_id, perf)
        if success:
            logger.info(f"✓ Performance Overview saved")
            saved_ids['performance'] = "overview"
        else:
            logger.error("✗ Failed to save performance overview")

        logger.info("\n" + "=" * 60)
        logger.info("✓ ALL DATA WRITTEN SUCCESSFULLY")
        logger.info("=" * 60)
        
        return saved_ids
        
    except Exception as e:
        logger.error(f"✗ Error writing data to Firebase: {e}")
        logger.exception("Full error details:")
        return None


def read_data_from_firebase(teacher_id: str, saved_ids: dict):
    """Read data from Firebase Firestore to verify connection"""
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 2: READING DATA FROM FIREBASE")
    logger.info("=" * 60)
    
    try:
        # 1. Read Teacher
        logger.info("\n[1/8] Reading Teacher...")
        teacher_data = TeacherService.get_teacher(teacher_id)
        if teacher_data:
            logger.info(f"✓ Teacher retrieved: {teacher_data.get('name')} ({teacher_data.get('email')})")
            logger.info(f"  Coverage: {teacher_data.get('coverage')}%, Topics: {teacher_data.get('total_topics')}")
        else:
            logger.error("✗ Failed to retrieve teacher")

        # 2. Read Syllabus
        logger.info("\n[2/8] Reading Syllabus...")
        if 'syllabus' in saved_ids:
            syllabus_data = SyllabusService.get_syllabus(teacher_id, saved_ids['syllabus'])
            if syllabus_data:
                logger.info(f"✓ Syllabus retrieved: {syllabus_data.get('file_name')}")
                logger.info(f"  Status: {syllabus_data.get('status')}, Year: {syllabus_data.get('academic_year')}")
            else:
                logger.error("✗ Failed to retrieve syllabus")
        else:
            logger.warning("⚠ Skipping syllabus read (not saved)")

        # 3. Read Test Paper
        logger.info("\n[3/8] Reading Test Paper...")
        if 'test_paper' in saved_ids:
            test_papers = TestPaperService.list_test_papers(teacher_id)
            if test_papers:
                logger.info(f"✓ Test Papers retrieved: {len(test_papers)} found")
                for tp in test_papers[:1]:  # Show first one
                    logger.info(f"  File: {tp.get('file_name')}, Status: {tp.get('status')}")
            else:
                logger.error("✗ No test papers found")
        else:
            logger.warning("⚠ Skipping test paper read (not saved)")

        # 4. Read Weak Areas
        logger.info("\n[4/8] Reading Weak Areas...")
        weak_areas = WeakAreaService.list_weak_areas(teacher_id)
        if weak_areas:
            logger.info(f"✓ Weak Areas retrieved: {len(weak_areas)} found")
            for wa in weak_areas[:1]:  # Show first one
                logger.info(f"  Topic: {wa.get('topic_name')}, Mastery: {wa.get('mastery')}%")
        else:
            logger.warning("⚠ No weak areas found")

        # 5. Read Recommendations
        logger.info("\n[5/8] Reading Recommendations...")
        recommendations = RecommendationService.list_recommendations(teacher_id)
        if recommendations:
            logger.info(f"✓ Recommendations retrieved: {len(recommendations)} found")
            for rec in recommendations[:1]:  # Show first one
                logger.info(f"  Recommendation: {rec.get('recommendation')}")
        else:
            logger.warning("⚠ No recommendations found")

        # 6. Read Uploads
        logger.info("\n[6/8] Reading Upload Records...")
        uploads = UploadService.list_uploads(teacher_id)
        if uploads:
            logger.info(f"✓ Uploads retrieved: {len(uploads)} found")
            for up in uploads[:1]:  # Show first one
                logger.info(f"  File: {up.get('file_name')}, Type: {up.get('file_type')}")
        else:
            logger.warning("⚠ No uploads found")

        # 7. Read Lesson Plans
        logger.info("\n[7/8] Reading Lesson Plans...")
        lesson_plans = LessonPlanService.list_lesson_plans(teacher_id)
        if lesson_plans:
            logger.info(f"✓ Lesson Plans retrieved: {len(lesson_plans)} found")
            for lp in lesson_plans[:1]:  # Show first one
                logger.info(f"  Topic: {lp.get('topic')}, Objectives: {len(lp.get('objectives', []))}")
        else:
            logger.warning("⚠ No lesson plans found")

        # 8. Read Performance Overview
        logger.info("\n[8/8] Reading Performance Overview...")
        perf_data = PerformanceService.get_overview(teacher_id)
        if perf_data:
            logger.info(f"✓ Performance Overview retrieved")
            logger.info(f"  Coverage: {perf_data.get('coverage')}%")
            logger.info(f"  Weak Areas: {perf_data.get('weak_areas_count')}")
        else:
            logger.error("✗ Failed to retrieve performance overview")

        logger.info("\n" + "=" * 60)
        logger.info("✓ ALL DATA READ SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info("\n🎉 Firebase Connection Test: PASSED")
        logger.info("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"✗ Error reading data from Firebase: {e}")
        logger.exception("Full error details:")


def main():
    """Main function to test Firebase connection"""
    teacher_id = "test_teacher_001"
    
    logger.info("\n" + "=" * 60)
    logger.info("FIREBASE FIRESTORE CONNECTION TEST")
    logger.info("=" * 60)
    logger.info(f"Teacher ID: {teacher_id}")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Phase 0: Upload files (PDF/Word docs) from backend root
    upload_results = upload_files_from_backend_root(teacher_id)
    
    if upload_results:
        successful_uploads = {k: v for k, v in upload_results.items() if v is not None}
        if successful_uploads:
            logger.info(f"\n{len(successful_uploads)} file(s) uploaded successfully. URLs saved.")
        else:
            logger.warning("No files were uploaded successfully. Continuing with other tests...")
    else:
        logger.warning("No files found to upload. Continuing with other tests...")
    
    # Phase 1: Write data
    saved_ids = write_data_to_firebase(teacher_id)
    
    if saved_ids:
        # Phase 2: Read data back
        read_data_from_firebase(teacher_id, saved_ids)
    else:
        logger.error("\n✗ Failed to write data. Cannot proceed with read test.")
        logger.error("Please check Firebase credentials and connection.")


if __name__ == "__main__":
    main()

