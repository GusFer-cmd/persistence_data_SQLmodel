from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Car, Manufacturer, CarSerieLink, Serie, CarRead
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/cars", tags=["Cars"])

#cars
@router.get("/", response_model=list[Car])
def list_cars(session: Session = Depends(get_session)):
    """
    Docstring para list_cars
    
    Args:
        session (Session): sessão do banco de dados

    Returns:
        List[Car]: lista com todos os carros 
    """
    cars = session.exec(select(Car)).all()
    return cars


@router.get("/paged", response_model=list[Car])
def list_cars_paged(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """
    Docstring para list_cars_paged
    
    Args:
        offset (int): deslocamento inicial
        limit (int): limite de registros a serem retornados
        session (Session): sessão do banco de dados

    Returns:
        List[Car]: lista com os carros dentro do intervalo fornecido
    """
    cars = session.exec(select(Car).offset(offset).limit(limit)).all()
    return cars

@router.post("/", response_model=Car)
def create_car(car: Car, session: Session = Depends(get_session)):
    """
    Docstring para create_car
    
    Args:
        car (Car): objeto carro a ser criado
        session (Session): sessão do banco de dados

    Returns:
        car (Car): carro criado 
    """
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

@router.get("/{car_id}", response_model=Car)
def get_car(car_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_car
    
    Args:
        car_id (int): id do carro desejado
        session (Session): sessão do banco de dados
    
    Returns:
        car (Car): carro com id car_id
    """
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.get("/{car_id}/series", response_model=CarRead)
def get_car_with_series(car_id: int, session: Session = Depends(get_session)):
    """
    Docstring para get_car_with_series

    Args:
        car_id (int): id do carro desejado
        session (Session): sessão do banco de dados
    
    Returns:
        car (Car): carro com suas series associadas
    """

    statement = (
        select(Car)
        .where(Car.id == car_id)
        .options(
            selectinload(Car.series)
            .selectinload(CarSerieLink.serie)
        )
    )

    car = session.exec(statement).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car

@router.put("/{car_id}", response_model=Car)
def update_car(car_id: int, updated_car: Car, session: Session = Depends(get_session)):
    """
    Docstring para update_car
    
    Args:
        car_id (int): id do carro a ser atualizado
        updated_car (Car): objeto carro com os novos dados
        session (Session): sessão do banco de dados
    
    Returns:
        car (Car): carro atualizado
    """
    car = session.get(Car, car_id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car.name = updated_car.name
    car.manufacturer = updated_car.manufacturer
    car.year = updated_car.year
    session.add(car)
    session.commit()
    session.refresh(car)
    
    return car

@router.delete("/{car_id}", response_model=Car)
def delete_car(car_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_car
    
    Args:
        car_id (int): id do carro a ser apagado
        session (Session): sessão do banco de dados
    
    Returns:
        car (Car): carro com id car_id (deletado do banco)
    """
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    session.delete(car)
    session.commit()
    return car

@router.get("/manufacturer/{manufacturer_id}", response_model=list[Car])
def list_cars_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_cars_manufacturer
    
    Args:
        manufacturer_id (int): id da montadora
        session (Session): sessão do banco de dados
    
    Returns:
        cars (List[Car]): lista com todos os carros da montadora com o id fornecido
    """
    query = select(Car).join(Manufacturer, Car.manufacturer_id == Manufacturer.id, isouter=True).where(Manufacturer.id == manufacturer_id)
    cars = session.exec(query)
    return cars

@router.get("/serie/{serie_id}", response_model=list[Car])
def list_cars_serie(serie_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_cars_serie
    
    Args:
        serie_id (int): id da serie
        session (Session): sessao do banco

    Returns:
        cars (List[Car]): lista de carros com a serie fornecida 
    """
    query = (select(Car)
            .join(CarSerieLink, CarSerieLink.car_id == Car.id, isouter=True)
            .join(Serie, CarSerieLink.serie_id == Serie.id, isouter=True)
            .where(Serie.year == serie_id))
    cars = session.exec(query)
    return cars

@router.get("/serie/year/{series_year}", response_model=list[Car])
def list_cars_series_year(series_year: int, session: Session = Depends(get_session)):
    """
    Docstring para list_cars_series_year
    
    Args:
        serie_year (int): ano da serie
        session (Session): sessao do banco

    Returns:
        cars (List[Car]): lista de carros pertencentes a series do ano fornecido 
    """
    query = (select(Car)
            .join(CarSerieLink, CarSerieLink.car_id == Car.id, isouter=True)
            .join(Serie, CarSerieLink.serie_id == Serie.id, isouter=True)
            .where(Serie.year == series_year))
    cars = session.exec(query)
    return cars