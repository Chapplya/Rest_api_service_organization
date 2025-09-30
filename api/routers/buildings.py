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
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(api_key.verify_api_key)],
)


def get_building_repository(db: Session = Depends(get_db)):
    return crud_resquests.BuildingRepository(db)


@router.post("/", response_model=schemas.Building)
def create_building(
    building: schemas.BuildingCreate,
    repo: crud_resquests.BuildingRepository = Depends(get_building_repository),
):
    return repo.create(obj_in=building)


@router.get("/", response_model=List[schemas.Building])
def read_buildings(
    skip: int = 0,
    limit: int = 100,
    repo: crud_resquests.BuildingRepository = Depends(get_building_repository),
):
    buildings = repo.get_multi(skip=skip, limit=limit)
    return buildings


@router.get("/{building_id}", response_model=schemas.Building)
def read_building(
    building_id: int,
    repo: crud_resquests.BuildingRepository = Depends(get_building_repository),
):
    building = repo.get(id=building_id)
    return building
