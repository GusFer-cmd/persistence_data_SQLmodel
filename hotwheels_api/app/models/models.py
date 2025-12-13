from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class Serie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    year: int

    cars: List["CarSerieLink"] = Relationship(back_populates="serie")

class Manufacturer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    scale: str
    color: str
    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")

    series: List["CarSerieLink"] = Relationship(back_populates="car")

    collections: List["CollectionCarLink"] = Relationship(back_populates="car")

class CarSerieLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    car_id: int = Field(foreign_key="car.id")
    serie_id: int = Field(foreign_key="serie.id")

    number: int
    max_number: int

    car: Optional[Car] = Relationship(back_populates="series")
    serie: Optional[Serie] = Relationship(back_populates="cars")

class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: str

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")

    cars: List["CollectionCarLink"] = Relationship(back_populates="collection")

class CollectionCarLink(SQLModel, table=True):
    collection_item_id: Optional[int] = Field(default=None, foreign_key="collection.id", primary_key=True)
    car_id: Optional[int] = Field(default=None, foreign_key="car.id", primary_key=True)
    added_date: datetime = Field(default_factory=datetime.now)

    collection: Optional[Collection] = Relationship(back_populates="cars")
    car: Optional[Car] = Relationship(back_populates="collections")
