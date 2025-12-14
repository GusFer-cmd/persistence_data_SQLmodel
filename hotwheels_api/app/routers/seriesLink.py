from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import CarSerieLink

router = APIRouter(prefix="/series_links", tags=["Series Links"])

#series cars links
@router.get("/", response_model=list[CarSerieLink])
def list_series_car_links(session: Session = Depends(get_session)):
    """
    Docstring para list_series_car_links
    
    Args:
        session (Session): sessao do banco

    Return:
        links (List[CarSerieLink]): lista com todas as associacoes de carros e series
    """
    links = session.exec(select(CarSerieLink)).all()
    return links

@router.post("/", response_model=CarSerieLink)
def create_series_car_link(link: CarSerieLink, session: Session = Depends(get_session)):
    """
    Docstring para create_series_car_link
    
    Args:
        link (CarSerieLink): objeto da tabela associativa entre Car e Series
        session (Session): sessao do banco
    
    Return:
        link (CarSerieLink):objeto da tabela associativa entre Car e Series adicionado ao banco
    """
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

@router.delete("/{car_id}/{serie_id}", response_model=CarSerieLink)
def delete_series_car_link(car_id: int, serie_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_series_car_link
    
    Args:
        car_id (int): id do carro
        serie_id (int): id da serie
        session (Session): sessao do banco
    
    Return:
        link (CarSerieLink):objeto da tabela associativa entre Car e Series deletado do banco
    """
    link = session.get(CarSerieLink, (car_id, serie_id))
    if not link:
        raise HTTPException(status_code=404, detail="Series Car Link not found")
    session.delete(link)
    session.commit()
    return link