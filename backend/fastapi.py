from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager 
from fastapi_login.exceptions import InvalidCredentialsException


app = FastAPI()


manager = LoginManager(SECRET, tokenUrl="/auth/login", use_cookie=True)
manager.cookie_name = "platform-cookie"

DB = {"username": {"password": "1234567"}} 


@manager.user_loader
def load_user(username: str):
   user = DB.get(username)
   return user


@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
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


@app.get("/public")
def getPublic():
   return "You are a user"


@ app.get("/auth/login",protected_route response_class=HTMLResponse)
async def login():
   return FileResponse("login.html")
   
   
@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request, user=Depends(manager)):
    resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, "")
    return resp


@app.post("/uploader/")
async def uploader(file: UploadFile):
    return Response(content=str("File Uploaded), media_type="text")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
