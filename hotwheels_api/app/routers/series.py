from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Serie, SerieWithCarsRead

router = APIRouter(prefix="/series", tags=["Series"])

#series
@router.get("/", response_model=list[Serie])
def list_series(session: Session = Depends(get_session)):
    """
    Docstring para list_series
    
    Args:
        session (Session): sessao do banco de dados

    Returns:
        series (List[Series]): lista de series
    """
    series = session.exec(select(Serie)).all()
    return series

@router.get("/paged", response_model=list[Serie])
def list_series_paged(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """
    Docstring para list_series_paged
    
    Args:
        offset (int): deslocamento inicial
        limit (int): limite de registros a serem retornados
        session (Session): sessão do banco de dados

    Returns:
        List[Serie]: lista com as series dentro do intervalo fornecido
    """
    series = session.exec(select(Serie).offset(offset).limit(limit)).all()
    return series
    
@router.post("/", response_model=Serie)
def create_serie(serie: Serie, session: Session = Depends(get_session)):
    """
    Docstring para create_serie
    
    Args:
        serie (Serie): objeto serie a ser inserido na tabela
        session (Session): sessao do banco

    Returns:
        serie (Serie): serie inserida no banco
    """
    session.add(serie)
    session.commit()
    session.refresh(serie)
    return serie

@router.get("/{serie_id}", response_model=Serie)
def list_serie(serie_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_serie
    
    Args:
        serie_id (int): id da serie
        session (Session): sessao do banco

    Returns:
        serie (Serie): objeto serie com  o id fornecido
    """
    serie = session.get(Serie, serie_id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    return serie

@router.get("/{serie_id}/cars", response_model=SerieWithCarsRead)
def get_serie_with_cars(serie_id: int, session: Session = Depends(get_session)):
    serie = session.exec(
        select(Serie).where(Serie.id == serie_id)
    ).first()

    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")

    return serie
    
@router.delete("/{serie_id}", response_model=Serie)
def delete_serie(serie_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_serie
    
    Args:
        serie_id (int): id da serie a ser deletada na tabela
        session (Session): sessao do banco

    Returns:
        serie (Serie): serie removida do banco
    """
    serie = session.get(Serie, serie_id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    session.delete(serie)
    session.commit()
    return serie

@router.get("/year/{serie_year}", response_model=list[Serie])
def list_serie_year(serie_year: int, session: Session = Depends(get_session)):
    """
    Docstring para list_serie_year
    
    Args:
    serie_year (int): ano da serie
    session (Session): sessao do banco

    Returns:
        series (List[Series]): lista com as series do ano fornecido
    """
    query = select(Serie).where(Serie.year == serie_year)
    series = session.exec(query)
    if not series:
        raise HTTPException(status_code=404, detail="Serie not found")
    return series
