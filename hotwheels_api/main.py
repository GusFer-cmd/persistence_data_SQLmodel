from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#Irá traduzir para colunas do banco de dados
class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class Serie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    year: int
    total: int

class Manufacturer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    scale: str
    color: str
    serie_id: Optional[int] = Field(default=None, foreign_key="serie.id")
    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")

class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: str
    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")

class CollectionCarLink(SQLModel, table=True):
    collection_item_id: Optional[int] = Field(default=None, foreign_key="collection.id", primary_key=True)
    car_id: Optional[int] = Field(default=None, foreign_key="car.id", primary_key=True)
    added_date: datetime = Field(default_factory=datetime.now)

#database 
sqlite_url = 'sqlite:///./hotwheels.db'
engine = create_engine(sqlite_url, echo=True)

#criando tabelas
def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="HotWheels API",
    description="API para gerenciamento de donos e suas coleções.",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#rotas

#owner
@app.get("/owners", response_model=list[Owner], tags=["Owners"])
def list_owners():
    with Session(engine) as session:
        owners = session.exec(select(Owner)).all()
        return owners
    
@app.get("/owner/{owner_id}", response_model=Owner, tags=["Owners"])
def list_owner(owner_id: int):
    with Session(engine) as session:
        owner = session.get(Owner, owner_id)
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")
        return owner
    
@app.post("/owners", response_model=Owner, tags=["Owners"])
def create_owner(owner: Owner):
    with Session(engine) as session:
        session.add(owner)
        session.commit()
        session.refresh(owner)
        return owner
    
@app.delete("/owner/{owner_id}", response_model=Owner, tags=["Owners"])
def delete_owner(owner_id: int):
    with Session(engine) as session:
        owner = session.get(Owner, owner_id)
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")
        session.delete(owner)
        session.commit()
        return owner

#manufacturer
@app.get("/manufactures", response_model=list[Manufacturer], tags=["Manufactures"])
def list_manufectures():
    with Session(engine) as session:
        manufectures = session.exec(select(Manufacturer)).all()
        return manufectures

@app.get("/manufacturer/{manufacturer_id}", response_model=Manufacturer, tags=["Manufactures"])
def list_manufecturer(manufacturer_id: int):
    with Session(engine) as session:
        manufacturer = session.get(Manufacturer, manufacturer_id)
        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        return manufacturer
    
@app.post("/manufactures", response_model=Manufacturer, tags=["Manufactures"])
def create_manufacturer(manufacturer: Manufacturer):
    with Session(engine) as session:
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        return manufacturer
    
@app.delete("/manufacturer/{manufacturer_id}", response_model=Manufacturer, tags=["Manufactures"])
def delete_manufacturer(manufacturer_id: int):
    with Session(engine) as session:
        manufacturer = session.get(Manufacturer, manufacturer_id)
        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")
        session.delete(manufacturer)
        session.commit()
        return manufacturer
    
#series
@app.get("/series/", response_model=list[Serie], tags=["Series"])
def list_series():
    with Session(engine) as session:
        series = session.exec(select(Serie)).all()
        return series
    
@app.post("/series", response_model=Serie, tags=["Series"])
def create_serie(serie: Serie):
    with Session(engine) as session:
        session.add(serie)
        session.commit()
        session.refresh(serie)
        return serie

@app.get("/serie{serie_id}", response_model=Serie, tags=["Series"])
def list_serie(serie_id: int):
    with Session(engine) as session:
        serie = session.get(Serie, serie_id)
        if not serie:
            raise HTTPException(status_code=404, detail="Serie not found")
        return serie
    
@app.delete("/serie/{serie_id}", response_model=Serie, tags=["Series"])
def delete_serie(serie_id: int):
    with Session(engine) as session:
        serie = session.get(Serie, serie_id)
        if not serie:
            raise HTTPException(status_code=404, detail="Serie not found")
        session.delete(serie)
        session.commit()
        return serie

#cars
@app.get("/cars", response_model=list[Car], tags=["Cars"])
def list_cars():
    with Session(engine) as session:
        cars = session.exec(select(Car)).all()
        return cars
    
@app.post("/cars", response_model=Car, tags=["Cars"])
def create_car(car: Car):
    with Session(engine) as session:
        session.add(car)
        session.commit()
        session.refresh(car)
        return car

@app.get("/car/{car_id}", response_model=Car, tags=["Cars"])
def list_car(car_id: int):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        return car
    
@app.delete("/car/{car_id}", response_model=Car, tags=["Cars"])
def delete_car(car_id: int):
    with Session(engine) as session:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        session.delete(car)
        session.commit()
        return car
    
#collection items
@app.get("/collection_items", response_model=list[Collection], tags=["Collection"])
def list_collection_items():
    with Session(engine) as session:
        items = session.exec(select(Collection)).all()
        return items

@app.post("/collection_items", response_model=Collection, tags=["Collection"])
def create_collection_item(item: Collection):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.get("/collection_item/{item_id}", response_model=Collection, tags=["Collection"])
def list_collection_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Collection, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Collection Item not found")
        return item
    
@app.delete("/collection_item/{item_id}", response_model=Collection, tags=["Collection"])
def delete_collection_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Collection, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Collection Item not found")
        session.delete(item)
        session.commit()
        return item
#teste
#collection car links
@app.get("/collection_car_links", response_model=list[CollectionCarLink], tags=["Collection Car Links"])
def list_collection_car_links():
    with Session(engine) as session:
        links = session.exec(select(CollectionCarLink)).all()
        return links
    
@app.post("/collection_car_links", response_model=CollectionCarLink, tags=["Collection Car Links"])
def create_collection_car_link(link: CollectionCarLink):
    with Session(engine) as session:
        session.add(link)
        session.commit()
        session.refresh(link)
        return link
    
@app.delete("/collection_car_link/{collection_item_id}/{car_id}", response_model=CollectionCarLink, tags=["Collection Car Links"])
def delete_collection_car_link(collection_item_id: int, car_id: int):
    with Session(engine) as session:
        link = session.get(CollectionCarLink, (collection_item_id, car_id))
        if not link:
            raise HTTPException(status_code=404, detail="Collection Car Link not found")
        session.delete(link)
        session.commit()
        return link
