from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar, Type
from sqlalchemy.orm import Session
from database import models, schemas
from fastapi import HTTPException, status

from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=schemas.BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=schemas.BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    @abstractmethod
    def get(self, id: int) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, obj_in: UpdateSchemaType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int) -> dict:
        raise NotImplementedError


class OrganizationRepository(
    BaseRepository[
        models.Organization, schemas.OrganizationCreate, schemas.OrganizationUpdate
    ]
):
    def __init__(self, db: Session):
        super().__init__(db, models.Organization)

    def get(self, id: int) -> Optional[models.Organization]:
        organization = self.db.query(self.model).filter(self.model.id == id).first()
        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена"
            )
        return organization

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[models.Organization]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: schemas.OrganizationCreate) -> models.Organization:
        db_organization = models.Organization(
            name=obj_in.name, building_id=obj_in.building_id
        )
        for phone_number in obj_in.phone_numbers:
            db_phone_number = models.PhoneNumber(
                number=phone_number.number, organization=db_organization
            )
            self.db.add(db_phone_number)

        self.db.add(db_organization)
        self.db.commit()
        self.db.refresh(db_organization)
        return db_organization

    def update(
        self, id: int, obj_in: schemas.OrganizationUpdate
    ) -> models.Organization:
        db_organization = self.get(id)
        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_organization, key, value)
        self.db.commit()
        self.db.refresh(db_organization)
        return db_organization

    def delete(self, id: int) -> dict:
        db_organization = self.get(id)
        self.db.delete(db_organization)
        self.db.commit()
        return {"message": "Организация успешно удалена"}

    def get_by_building(self, building_id: int) -> List[models.Organization]:
        return (
            self.db.query(self.model)
            .filter(self.model.building_id == building_id)
            .all()
        )

    def get_by_activity(self, activity_id: int) -> List[models.Organization]:
        activity = (
            self.db.query(models.Activity)
            .filter(models.Activity.id == activity_id)
            .first()
        )
        if not activity:
            raise HTTPException(status_code=404, detail="Вид деятельности не найден")
        return activity.organizations

    def search_by_activity(self, activity_name: str) -> List[models.Organization]:
        activities = (
            self.db.query(models.Activity)
            .filter(models.Activity.name.ilike(f"%{activity_name}%"))
            .all()
        )
        organizations = set()
        for activity in activities:
            organizations.update(activity.organizations)

            def get_child_organizations(parent_activity, level):
                if level > 3:
                    return
                for child_activity in parent_activity.children:
                    organizations.update(child_activity.organizations)
                    get_child_organizations(child_activity, level + 1)

            get_child_organizations(activity, 1)

        return list(organizations)

    def search_by_name(self, name: str) -> List[models.Organization]:
        return (
            self.db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()
        )


class BuildingRepository(BaseRepository[models.Building, schemas.BuildingCreate, None]):
    def __init__(self, db: Session):
        super().__init__(db, models.Building)

    def get(self, id: int) -> Optional[models.Building]:
        building = self.db.query(self.model).filter(self.model.id == id).first()
        if building is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Здание не найдено"
            )
        return building

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[models.Building]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: schemas.BuildingCreate) -> models.Building:
        db_building = models.Building(
            address=obj_in.address, latitude=obj_in.latitude, longitude=obj_in.longitude
        )
        self.db.add(db_building)
        self.db.commit()
        self.db.refresh(db_building)
        return db_building

    def update(self, id: int, obj_in: None) -> models.Building:
        raise NotImplementedError("Метод Update для Building не реализован")

    def delete(self, id: int) -> dict:
        raise NotImplementedError("Метод Delete для Building не реализован")


class ActivityRepository(
    BaseRepository[models.Activity, schemas.ActivityCreate, None]
):  # Update не нужен
    def __init__(self, db: Session):
        super().__init__(db, models.Activity)

    def get(self, id: int) -> Optional[models.Activity]:
        activity = self.db.query(self.model).filter(self.model.id == id).first()
        if activity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вид деятельности не найден",
            )
        return activity

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[models.Activity]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: schemas.ActivityCreate) -> models.Activity:
        db_activity = models.Activity(name=obj_in.name, parent_id=obj_in.parent_id)
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity

    def update(self, id: int, obj_in: None) -> models.Activity:
        raise NotImplementedError("Метод Update для Activity не реализован")

    def delete(self, id: int) -> dict:
        raise NotImplementedError("Метод Delete для Activity не реализован")
