from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import CollectionCarLink

router = APIRouter(prefix="/collection_car_links", tags=["Collection Car Links"])

#collection car links
@router.get("/", response_model=list[CollectionCarLink])
def list_collection_car_links(session: Session = Depends(get_session)):
    links = session.exec(select(CollectionCarLink)).all()
    return links
    
@router.post("/", response_model=CollectionCarLink)
def create_collection_car_link(link: CollectionCarLink, session: Session = Depends(get_session)):
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
    
@router.delete("/{collection_item_id}/{car_id}", response_model=CollectionCarLink)
def delete_collection_car_link(collection_item_id: int, car_id: int, session: Session = Depends(get_session)):
    link = session.get(CollectionCarLink, (collection_item_id, car_id))
    if not link:
        raise HTTPException(status_code=404, detail="Collection Car Link not found")
    session.delete(link)
    session.commit()
    return link
