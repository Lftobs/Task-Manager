from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.todo_routes import todo_r
from app.config import Settings

# 3rd party
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth)
app.include_router(todo_r)

    
