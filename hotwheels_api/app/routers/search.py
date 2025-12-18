from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Car, CarSerieLink, Serie, CarRead, CollectionCarLinkRead, SerieWithCarsRead, CollectionCarLink, Owner, Collection, CollectionRead
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/cars/", response_model=list[CarRead])
def search_cars_by_name(name: str, offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """
    Search cars by name with pagination.
    
    Args:
        name (str): name or part of the name of the car to search for
        offset (int): initial offset
        limit (int): limit of records to be returned
        session (Session): database session

    Returns:
        List[CarRead]: list of cars matching the search criteria within the provided range
    """
    statement = select(Car).where(Car.name.ilike(f"%{name}%")).offset(offset).limit(limit).options(selectinload(Car.series).selectinload(CarSerieLink.serie))
    cars = session.exec(statement).all()

    return cars

@router.get("/collections/{collection_id}/cars/", response_model=list[CollectionCarLinkRead])
def search_cars_in_collection_by_name(collection_id: int, name: str, session: Session = Depends(get_session)):
    """
    Search cars in a specific collection by name.
    
    Args:
        collection_id (int): ID of the collection
        name (str): name or part of the name of the car to search for
        session (Session): database session
    Returns:
        List[CollectionCarLinkRead]: list of cars in the collection matching the search criteria
    """
    statement = select(CollectionCarLink).where(
        CollectionCarLink.collection_item_id == collection_id,
        CollectionCarLink.car.has(Car.name.ilike(f"%{name}%"))
    ).options(selectinload(CollectionCarLink.car).selectinload(Car.series).selectinload(CarSerieLink.serie))
    
    collection_cars = session.exec(statement).all()

    if not collection_cars:
        raise HTTPException(status_code=404, detail="No cars found in the specified collection with the given name.")

    return collection_cars

@router.get("/series/{series_name}/cars/", response_model=list[SerieWithCarsRead])
def search_series_by_name_with_cars(series_name: str, session: Session = Depends(get_session)):
    """
    Search series by name and return all cars in the series with details.
    
    Args:
        series_name (str): name or part of the name of the series to search for
        session (Session): database session

    Returns:
        List[SerieWithCarsRead]: list of series matching the search criteria with their cars
    """
    statement = select(Serie).where(Serie.name.ilike(f"%{series_name}%")).options(selectinload(Serie.cars).selectinload(CarSerieLink.car))
    series_list = session.exec(statement).all()

    if not series_list:
        raise HTTPException(status_code=404, detail="No series found with the given name.")

    return series_list

@router.get("owner/{owner_name}", response_model=list[CollectionRead])
def search_owner_collections(owner_name: str, session: Session = Depends(get_session)):
    """
    Search for owners by name and return their collections with cars.

    Args:
        owner_name (str): Name or part of the name of the owner to search for
        session (Session): Database session

    Returns:
        List[OwnerWithCollectionsRead]: List of owners with their collections and cars
    """
    statement = (
        select(Collection)
        .join(Owner, Collection.owner_id == Owner.id)
        .where(Owner.name.ilike(f"%{owner_name}%"))
        .options(
            selectinload(Collection.cars).selectinload(CollectionCarLink.car)
        )
    )

    owners = session.exec(statement).all()

    if not owners:
        raise HTTPException(status_code=404, detail="No owners found with the given name.")

    return owners
