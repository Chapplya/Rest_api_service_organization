from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from geoalchemy2 import Geometry
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


organization_activity_association = Table(
    "organization_activity",
    Base.metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id"), primary_key=True
    ),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="organizations")
    activities = relationship(
        "Activity",
        secondary=organization_activity_association,
        back_populates="organizations",
    )
    phone_numbers = relationship("PhoneNumber", back_populates="organization")


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phone_numbers")


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    # location = Column(Geometry(geometry_type="POINT", srid=4326))  # SRID 4326 - WGS 84

    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(
        Integer, ForeignKey("activities.id"), nullable=True
    )  # Ссылка на родительскую категорию

    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")

    organizations = relationship(
        "Organization",
        secondary=organization_activity_association,
        back_populates="activities",
    )

    @hybrid_property
    def level(self):
        if self.parent:
            return self.parent.level + 1
        return 1

    @level.setter
    def level(self, level):
        pass
