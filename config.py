# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://user:password@db:5432/mydatabase"
    )
    API_KEY: str = os.getenv("API_KEY", "super_secret_api_key")  # Статический API ключ


settings = Settings()
