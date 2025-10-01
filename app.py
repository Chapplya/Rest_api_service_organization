# app/main.py
from fastapi import FastAPI
from database.models import Base
from api import register_routers

from database.connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Справочник Организаций, Зданий, Деятельности",
    description="REST API для управления справочником организаций, зданий и видов деятельности.",
    version="0.1.0",
)

register_routers(app)


