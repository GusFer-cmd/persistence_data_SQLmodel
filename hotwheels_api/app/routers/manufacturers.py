from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from app.core.database import get_session
from app.models.models import Manufacturer, Car

router = APIRouter(prefix="/manufactures", tags=["Manufactures"])

#manufacturer
@router.get("/", response_model=list[Manufacturer])
def list_manufactures(session: Session = Depends(get_session)):
    """
    Docstring para list_manufactures
    
    Args:
        session (Session): sessao do banco de dados
    
    Returns:
        manufactures (List[Manufacturer]): lista de todas as montadoras
    """
    manufactures = session.exec(select(Manufacturer)).all()
    return manufactures

@router.get("/paged", response_model=list[Manufacturer])
def list_manufactureres_paged(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """
    Docstring para list_manufactures_paged
    
    Args:
        offset (int): deslocamento inicial
        limit (int): limite de registros a serem retornados
        session (Session): sessao do banco
    
    Returns:
        collection (List[Manufacturer]): lista com as montadoras dentro do intervalo fornecido
    """
    manufactureres = session.exec(select(Manufacturer).offset(offset).limit(limit)).all()
    return manufactureres
    
@router.post("/", response_model=Manufacturer)
def create_manufacturer(manufacturer: Manufacturer, session: Session = Depends(get_session)):
    """
    Docstring para create_manufacturer
    
    Args:
        manufacturer (Manufacturer): objeto Manufacturer a ser inserido no banco
        session (Session): sessao do banco de dados
    
    Returns:
        manufacturer (Manufacturer): objeto Manufacturer que foi inserido no banco
    """
    session.add(manufacturer)
    session.commit()
    session.refresh(manufacturer)
    return manufacturer

@router.get("/{manufacturer_id}", response_model=Manufacturer)
def get_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    """
    Docstring para get_manufacturer
    
    Args:
        manufacturer_id (int): id da montadora
        session (Session): sessao do banco

    Returns:
        manufacturer (Manufacturer): montadora com o id fornecido
    """
    manufacturer = session.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer
    
@router.delete("/{manufacturer_id}", response_model=Manufacturer)
def delete_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_manufacturer
    
    Args:
        manufacturer_id (int): id do objeto Manufacturer a ser removido
        session (Session): sessao do banco de dados
    
    Returns:
        manufacturer (Manufacturer): objeto Manufacturer que foi deletado do banco
    """
    manufacturer = session.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    session.delete(manufacturer)
    session.commit()
    return manufacturer

@router.get("/quantity/{numb}", response_model=list[Manufacturer])
def list_manufactures_number(numb: int, session: Session = Depends(get_session)):
    """
    Docstring para list_manufactures_number
    
    numb (int): numero minimo de carros
    session (Session): sessao do banco de dados

    manufactures (List[Manufacturer]): lista com as montadoras com mais que numb carros
    """
    query = (select(Manufacturer)
                .join(Car, Car.manufacturer_id == Manufacturer.id)
                .group_by(Manufacturer.id)
                .having(func.count(Car.manufacturer_id) >= numb)
                .distinct())
    manufactures = session.exec(query)
    return manufactures