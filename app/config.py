import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BASE_URL: str
    HTML_CACHE_DIR: str

    def __init__(self):
        
        super().__init__()

        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
        self.BASE_URL = os.getenv("BASE_URL", "")
        self.HTML_CACHE_DIR = os.getenv("HTML_CACHE_DIR", "")


@lru_cache()
def get_settings():
    return Settings()