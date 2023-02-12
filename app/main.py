from fastapi import FastAPI
from app.routes import auth
from app.todo_routes import todo_r
from fastapi_jwt_auth import AuthJWT
from app.config import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth)
app.include_router(todo_r)