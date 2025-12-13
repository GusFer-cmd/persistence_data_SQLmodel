from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Car, Manufacturer, CarSerieLink, Serie

router = APIRouter(prefix="/cars", tags=["Cars"])

#cars
@router.get("/", response_model=list[Car])
def list_cars(session: Session = Depends(get_session)):
    cars = session.exec(select(Car)).all()
    return cars

@router.post("/", response_model=Car)
def create_car(car: Car, session: Session = Depends(get_session)):
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

@router.get("/{car_id}", response_model=Car)
def list_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car
    
@router.delete("/{car_id}", response_model=Car)
def delete_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    session.delete(car)
    session.commit()
    return car

@router.get("/manufacturer/{manufacturer_id}", response_model=list[Car])
def list_cars_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    query = select(Car).join(Manufacturer, Car.manufacturer_id == Manufacturer.id, isouter=True).where(Manufacturer.id == manufacturer_id)
    cars = session.exec(query)
    return cars

@router.get("/serie/{serie_id}", response_model=list[Car])
def list_cars_serie(serie_id: int, session: Session = Depends(get_session)):
    query = (select(Car)
            .join(CarSerieLink, CarSerieLink.car_id == Car.id, isouter=True)
            .join(Serie, CarSerieLink.serie_id == Serie.id, isouter=True)
            .where(Serie.year == serie_id))
    cars = session.exec(query)
    return cars

@router.get("/serie/year/{series_year}", response_model=list[Car])
def list_cars_series_year(series_year: int, session: Session = Depends(get_session)):
    query = (select(Car)
            .join(CarSerieLink, CarSerieLink.car_id == Car.id, isouter=True)
            .join(Serie, CarSerieLink.serie_id == Serie.id, isouter=True)
            .where(Serie.year == series_year))
    cars = session.exec(query)
    return cars