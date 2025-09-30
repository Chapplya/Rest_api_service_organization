from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import schemas
from database.connection import get_db
from api.security import api_key
from api.repositories import crud_resquests
from typing import List

from database import schemas

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(api_key.verify_api_key)],
)


def get_organization_repository(db: Session = Depends(get_db)):
    return crud_resquests.OrganizationRepository(db)


@router.post("/", response_model=schemas.Organization)
def create_organization(
    organization: schemas.OrganizationCreate,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    return repo.create(obj_in=organization)


@router.get("/", response_model=List[schemas.Organization])
def read_organizations(
    skip: int = 0,
    limit: int = 100,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organizations = repo.get_multi(skip=skip, limit=limit)
    return organizations


@router.get("/{organization_id}", response_model=schemas.Organization)
def read_organization(
    organization_id: int,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organization = repo.get(id=organization_id)
    return organization


@router.put("/{organization_id}", response_model=schemas.Organization)
def update_organization(
    organization_id: int,
    organization: schemas.OrganizationUpdate,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    return repo.update(id=organization_id, obj_in=organization)


@router.delete("/{organization_id}")
def delete_organization(
    organization_id: int,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    return repo.delete(id=organization_id)


@router.get("/by_building/{building_id}", response_model=List[schemas.Organization])
def read_organizations_by_building(
    building_id: int,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organizations = repo.get_by_building(building_id=building_id)
    return organizations


@router.get("/by_activity/{activity_id}", response_model=List[schemas.Organization])
def read_organizations_by_activity(
    activity_id: int,
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organizations = repo.get_by_activity(activity_id=activity_id)
    return organizations


@router.get("/search_by_activity/", response_model=List[schemas.Organization])
def search_organizations_by_activity(
    activity_name: str = Query(..., title="Название вида деятельности"),
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organizations = repo.search_by_activity(activity_name=activity_name)
    return organizations


@router.get("/search_by_name/", response_model=List[schemas.Organization])
def search_organizations_by_name(
    name: str = Query(..., title="Название организации"),
    repo: crud_resquests.OrganizationRepository = Depends(get_organization_repository),
):
    organizations = repo.search_by_name(name=name)
    return organizations
