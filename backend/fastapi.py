from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager 
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import Depends, Request, UploadFile, Response, Form, status
import json, os
import shutil
from google import genai
from models import teacher, lesson_plan, performance_overview, recommendation, weak_area, upload_record, test_paper, syllabus
from services import teacher_service, lesson_plan_service, performance_service, recommendation_service, weak_area_service, storage_service, upload_service, test_paper_service, syllabus_service


app = FastAPI()


SECRET = "FirstSecretWord"
teacher_id = "VirtualTour"
os.environ["GEMINI_API_KEY"] = 'YOUR_API_KEY'


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
manager = LoginManager(SECRET, token_url="/auth/login", use_cookie=True)
manager.cookie_name = "platform-cookie"


DB = {"username": {"password": "1234567"}} 


@manager.user_loader
def load_user(username: str):
   user = DB.get(username)
   return user


@app.get("/")
async def read_root():
    return {"message": "Welcome to the new innovative project!"}


@app.post("/submit_teacher/")
async def submit_teacher_form(name: str = Form(...), email: str = Form(...)):
    newteacher = teacher.Teacher(name=name, email=email)
    teacher_service.TeacherService.save_teacher(newteacher)
    return {"Form received"}


@app.post("/get_teacher/")
async def get_teacher():
    teacher =teacher_service.TeacherService.get_teacher(teacher_id)
    return {json.dumps(teacher)}


@app.post("/update_teacher/")
async def teacher_update(field: str = Form(...), value: str = Form(...)):
    teacher_service.TeacherService.update_field(teacher_id, field, value)
    return {"Form received"}


@app.post("/add_lesson/")
async def add_lesson_form(lessonplan: lesson_plan.LessonPlan):
    lesson_plan_service.LessonPlanService.add_lesson_plan(teacher_id, lessonplan)
    return {"Form received"}


@app.post("/save_lesson/")
async def save_lesson_form(plan_id: str = Form(...), lessonplan: lesson_plan.LessonPlan = Depends()):
    lesson_plan_service.LessonPlanService.save_lesson_plan(teacher_id, plan_id, lessonplan)
    return {"Form received"}


@app.post("/list_lessons/")
async def list_lessons():
    lessons = lesson_plan_service.LessonPlanService.list_lesson_plans(teacher_id)
    return {json.dumps(lessons)}


@app.post("/performance_save/")
async def performance_save(performance: performance_overview.PerformanceOverview):
    performance_service.PerformanceService.save_overview(teacher_id, performance)
    return {"Form received"}


@app.post("/performance_overview/")
async def list_performances():
    performances = performance_service.PerformanceService.get_overview(teacher_id)
    return {json.dumps(performances)}


@app.post("/add_recommendation/")
async def add_recommendation_form(recommendation: recommendation.Recommendation):
    recommendation_service.RecommendationService.add_recommendation(teacher_id, recommendation)
    return {"Form received"}


@app.post("/save_recommendation/")
async def save_recommendation_form(rec_id: str = Form(...), recommendation: recommendation.Recommendation = Depends()):
    recommendation_service.RecommendationService.save_recommendation(teacher_id, rec_id, recommendation)
    return {"Form received"}


@app.post("/list_recommendations/")
async def list_recommendations():
    recommendations = recommendation_service.RecommendationService.list_recommendations(teacher_id)
    return {json.dumps(recommendations)}


@app.post("/add_weak_area/")
async def add_weak_area_form(weakarea: weak_area.WeakArea):
   weak_area_service.WeakAreaService.add_weak_area(teacher_id, weakarea)
   return {"Form received"}


@app.post("/save_weak_area/")
async def save_weak_area_form(topic_id: str = Form(...), weakarea: weak_area.WeakArea = Depends()):
    weak_area_service.WeakAreaService.save_weak_area(teacher_id, topic_id, weakarea)
    return {"Form received"}


@app.post("/list_weak_areas/")
async def list_weak_areas():
    weakareas = weak_area_service.WeakAreaService.list_weak_areas(teacher_id)
    return {json.dumps(weakareas)}


@app.post("/auth/login")
def login_handling(data: OAuth2PasswordRequestForm = Depends()):
   username = data.username
   password = data.password
   user = load_user(username)
   if not user:
       raise InvalidCredentialsException
   elif password != user['password']:
       raise InvalidCredentialsException
   access_token = manager.create_access_token(
       data={"sub": username}
   )
   resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)
   manager.set_cookie(resp, access_token)
   return resp


@app.get("/private")
def getPrivate(_=Depends(manager)):
   return "You are an authentciated user"


@app.get("/gemini")
def getGemini(_=Depends(manager)):
   response = client.models.generate_content(model='gemini-2.0-flash', contents='What could we learn on a Monday?')
   return "What answer do you expect?"


@app.get("/public")
def getPublic():
   return "You are a user"


@ app.get("/auth/login", response_class=HTMLResponse)
async def login():
   return FileResponse("login.html")
   
   
@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request, user=Depends(manager)):
    resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, "")
    return resp


@app.post("/uploader/")
async def uploader(file: UploadFile):
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = storage_service.StorageService.upload_file(save_path)
    upload_data = upload_record.UploadRecord(str(file.filename), "TextDocument", url)
    upload_service.UploadService.add_upload(teacher_id, upload_data)
    return Response(content=str("File Uploaded"), media_type="text")


@app.post("/list_uploads/")
async def list_uploads():
    uploads = upload_service.UploadService.list_uploads(teacher_id)
    return {json.dumps(uploads)}


@app.post("/test_paper_uploader/")
async def test_paper_uploader(file: UploadFile):
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = storage_service.StorageService.upload_file(save_path)
    upload_data = upload_record.UploadRecord(str(file.filename), "TestPaper", url)
    upload_service.UploadService.add_upload(teacher_id, upload_data)
    testpaper_upload_data = test_paper.TestPaper(str(file.filename), url) 
    test_paper_service.TestPaperService.add_test_paper(teacher_id, testpaper_upload_data)
    return Response(content=str("File Uploaded"), media_type="text")


@app.post("/list_testpaper_uploads/")
async def list_testpaper_uploads():
    uploads = test_paper_service.TestPaperService.list_test_papers(teacher_id)
    return {json.dumps(uploads)}


@app.post("/syllabus_uploader/")
async def syllabus_uploader(file: UploadFile):
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = storage_service.StorageService.upload_file(save_path)
    upload_data = upload_record.UploadRecord(str(file.filename), "TestPaper", url)
    upload_service.UploadService.add_upload(teacher_id, upload_data)
    syllabus_upload_data = syllabus.Syllabus(str(file.filename), url) 
    syllabus_service.SyllabusService.add_syllabus(teacher_id, syllabus_upload_data)
    return Response(content=str("File Uploaded"), media_type="text")


@app.post("/list_syllabus_uploads/")
async def list_syllabus_uploads():
    uploads = syllabus_service.SyllabusService.list_syllabi(teacher_id)
    return {json.dumps(uploads)}

