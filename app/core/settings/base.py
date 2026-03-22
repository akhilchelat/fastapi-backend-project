from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
   
    APP_NAME: str = "FastAPI Backend"
    ENVIRONMENT: str = "production"

    
    DATABASE_URL: str

    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
