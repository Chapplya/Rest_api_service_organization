# app/main.py
from fastapi import FastAPI, Depends
from database.models import Base
from api.security import api_key
from api.routers import organizations, buildings, activities
from database.connection import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Справочник Организаций, Зданий, Деятельности",
    description="REST API для управления справочником организаций, зданий и видов деятельности.",
    version="0.1.0",
)

app.include_router(organizations.router)
app.include_router(buildings.router)
app.include_router(activities.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Добро пожаловать в API справочника Организаций!"}


# Пример защищенного эндпоинта
@app.get(
    "/protected-route",
    tags=["Protected"],
    dependencies=[Depends(api_key.verify_api_key)],
)
async def get_protected_data():
    return {
        "message": "Вы успешно аутентифицированы и получили доступ к защищенным данным."
    }
