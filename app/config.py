from pydantic import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    authjwt_secret_key: str


    class Config:
        env_file = ".env"

settings = Settings()