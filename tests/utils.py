from sqlalchemy.orm import Session
from database import models


def create_test_organization(db: Session, name: str = "Test Organization"):
    organization = models.Organization(name=name)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def create_test_building(
    db: Session,
    address: str = "Test Building Address",
    latitude: float = 0.0,
    longitude: float = 0.0,
):

    building = models.Building(address=address, latitude=latitude, longitude=longitude)
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


def create_test_activity(db: Session, name: str = "Test Activity"):
    activity = models.Activity(name=name)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
