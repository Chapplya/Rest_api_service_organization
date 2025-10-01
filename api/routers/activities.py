from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import schemas
from database.connection import get_db
from api.security import api_key
from api.repositories import crud_resquests
from typing import List

from database import schemas


router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(api_key.verify_api_key)],
)


@router.get("/", tags=["Root"])
async def read_root():
    return {"message": "Добро пожаловать в API справочника Организаций!"}


@router.get(
    "/protected-route",
    tags=["Protected"],
    dependencies=[Depends(api_key.verify_api_key)],
)
async def get_protected_data():
    return {
        "message": "Вы успешно аутентифицированы и получили доступ к защищенным данным."
    }


def get_activity_repository(db: Session = Depends(get_db)):
    return crud_resquests.ActivityRepository(db)


@router.post("/", response_model=schemas.Activity)
def create_activity(
    activity: schemas.ActivityCreate,
    repo: crud_resquests.ActivityRepository = Depends(get_activity_repository),
):
    return repo.create(obj_in=activity)


@router.get("/", response_model=List[schemas.Activity])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    repo: crud_resquests.ActivityRepository = Depends(get_activity_repository),
):
    activities = repo.get_multi(skip=skip, limit=limit)
    return activities


@router.get("/{activity_id}", response_model=schemas.Activity)
def read_activity(
    activity_id: int,
    repo: crud_resquests.ActivityRepository = Depends(get_activity_repository),
):
    activity = repo.get(id=activity_id)
    return activity
