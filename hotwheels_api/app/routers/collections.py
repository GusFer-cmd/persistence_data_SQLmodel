from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Collection

router = APIRouter(prefix="/collection", tags=["Collection"])

#collection items
@router.get("/", response_model=list[Collection])
def list_collection_items(session: Session = Depends(get_session)):
    items = session.exec(select(Collection)).all()
    return items

@router.post("/", response_model=Collection)
def create_collection_item(item: Collection, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
    
@router.get("/{item_id}", response_model=Collection)
def list_collection_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Collection, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Collection Item not found")
    return item
    
@router.delete("/{item_id}", response_model=Collection)
def delete_collection_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Collection, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Collection Item not found")
    session.delete(item)
    session.commit()
    return item