from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse                     from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager                                           from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import Depends, Request, UploadFile                                 import json, os
from google import genai                                                         
                                                                                 app = FastAPI()
                                                                                 
SECRET = "FirstSecretWord"                                                       os.environ["GEMINI_API_KEY"] = 'YOUR_API_KEY'
                                                                                 
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])                      manager = LoginManager(SECRET, token_url="/auth/login", use_cookie=True)
manager.cookie_name = "platform-cookie"                                          
                                                                                 

DB = {"username": {"password": "1234567"}}

                                                                                 
@manager.user_loader                                                             def load_user(username: str):
   user = DB.get(username)                                                          return user

                                                                                 
@app.get("/")                                                                    async def read_root():
        return {"message": "Welcome to the new innovative project!"} 


@app.post("/submit_teacher/")
async def submit_teacher_form(name: str = Form(...), email: str = Form(...)):
    return {"Form received"}
            
                                                                                 
@app.post("/auth/login")                                                         def login(data: OAuth2PasswordRequestForm = Depends()):
   username = data.username                                                         password = data.password
   user = load_user(username)                                                       if not user:
       raise InvalidCredentialsException                                            elif password != user['password']:
       raise InvalidCredentialsException                                            access_token = manager.create_access_token(
       data={"sub": username}                                                       )
   resp = RedirectResponse(url="/private", status_code=status.HTTP_302_FOUND)       manager.set_cookie(resp, access_token)
   return resp
                                                                   
                                                                                 @app.get("/private")
def getPrivate(_=Depends(manager)):                                                 return "You are an authentciated user"

                                                                                 
@app.get("/gemini")                                                              def getGemini(_=Depends(manager)):
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
    return Response(content=str("File Uploaded"), media_type="text")