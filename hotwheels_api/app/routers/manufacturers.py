from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Manufacturer

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