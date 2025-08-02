from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from vern_backend.app.agents import router as agents_router
from vern_backend.app.plugins import router as plugins_router
from vern_backend.app.users import router as users_router

app = FastAPI(
    title="VERN Backend API",
    description="Modular FastAPI backend for agent orchestration, plugin registry, and user/session management.",
    version="0.1.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: Validate JWT token and return user info
    if not token or token == "fake":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return {"user_id": "default_user"}

app.include_router(agents_router)
app.include_router(plugins_router)
app.include_router(users_router)

@app.get("/")
def read_root():
    return {"message": "VERN Backend API is running."}

@app.get("/secure-status")
def secure_status(user=Depends(get_current_user)):
    return {"status": "secure", "user": user}
