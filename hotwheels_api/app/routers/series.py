from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Serie

router = APIRouter(prefix="/series", tags=["Series"])

#series
@router.get("/", response_model=list[Serie])
def list_series(session: Session = Depends(get_session)):
    series = session.exec(select(Serie)).all()
    return series
    
@router.post("/", response_model=Serie)
def create_serie(serie: Serie, session: Session = Depends(get_session)):
    session.add(serie)
    session.commit()
    session.refresh(serie)
    return serie

@router.get("/{serie_id}", response_model=Serie)
def list_serie(serie_id: int, session: Session = Depends(get_session)):
    serie = session.get(Serie, serie_id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    return serie
    
@router.delete("/{serie_id}", response_model=Serie)
def delete_serie(serie_id: int, session: Session = Depends(get_session)):
    serie = session.get(Serie, serie_id)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    session.delete(serie)
    session.commit()
    return serie

@router.get("/year/{serie_year}", response_model=list[Serie])
def list_serie_year(serie_year: int, session: Session = Depends(get_session)):
    query = select(Serie).where(Serie.year == serie_year)
    serie = session.exec(query)
    if not serie:
        raise HTTPException(status_code=404, detail="Serie not found")
    return serie
