from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.core.database import get_session
from app.models.models import Manufacturer, Car

router = APIRouter(prefix="/manufactures", tags=["Manufactures"])

#manufacturer
@router.get("/", response_model=list[Manufacturer])
def list_manufectures(session: Session = Depends(get_session)):
    manufectures = session.exec(select(Manufacturer)).all()
    return manufectures
    
@router.post("/", response_model=Manufacturer)
def create_manufacturer(manufacturer: Manufacturer, session: Session = Depends(get_session)):
    session.add(manufacturer)
    session.commit()
    session.refresh(manufacturer)
    return manufacturer

@router.get("/{manufacturer_id}", response_model=Manufacturer)
def list_manufecturer(manufacturer_id: int, session: Session = Depends(get_session)):
    manufacturer = session.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer
    
@router.delete("/{manufacturer_id}", response_model=Manufacturer)
def delete_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    manufacturer = session.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    session.delete(manufacturer)
    session.commit()
    return manufacturer

@router.get("/quantity/{numb}", response_model=list[Manufacturer])
def list_manufectures_number(numb: int, session: Session = Depends(get_session)):
    query = (select(Manufacturer)
                .join(Car, Car.manufacturer_id == Manufacturer.id)
                .group_by(Manufacturer.id)
                .having(func.count(Car.manufacturer_id) >= numb)
                .distinct())
    manufectures = session.exec(query)
    return manufectures