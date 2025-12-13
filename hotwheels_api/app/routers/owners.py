from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Owner

router = APIRouter(prefix="/owners", tags=["Owners"])

#owner
@router.get("/", response_model=list[Owner])
def list_owners(session: Session = Depends(get_session)):
    owners = session.exec(select(Owner)).all()
    return owners
    
@router.post("/", response_model=Owner)
def create_owner(owner: Owner, session: Session = Depends(get_session)):
    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner
    
@router.get("/{owner_id}", response_model=Owner)
def list_owner(owner_id: int, session: Session = Depends(get_session)):
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner
    
@router.delete("/{owner_id}", response_model=Owner)
def delete_owner(owner_id: int, session: Session = Depends(get_session)):
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    session.delete(owner)
    session.commit()
    return owner