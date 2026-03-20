from app.core.settings.base import AppSettings

class Settings(AppSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()