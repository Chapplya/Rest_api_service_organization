# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    API_KEY: str = os.getenv("API_KEY")

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()
