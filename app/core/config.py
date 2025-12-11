import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "fintruck-internal")


settings = Settings()
