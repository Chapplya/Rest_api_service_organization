from pydantic import BaseModel
from typing import List, Optional


class PhoneNumberBase(BaseModel):
    number: str


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumber(PhoneNumberBase):
    id: int
    organization_id: int

    class Config:
        orm_mode = True


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    level: int

    class Config:
        orm_mode = True


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    phone_numbers: List[PhoneNumberCreate] = []


class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None
    building_id: Optional[int] = None


class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity]
    phone_numbers: List[PhoneNumber]

    class Config:
        orm_mode = True
