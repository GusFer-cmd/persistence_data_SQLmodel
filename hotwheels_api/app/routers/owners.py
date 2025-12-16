from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Owner

router = APIRouter(prefix="/owners", tags=["Owners"])

#owner
@router.get("/", response_model=list[Owner])
def list_owners(session: Session = Depends(get_session)):
    """
    Docstring para list_owners
    
    Args:
        session (Session): sessao do banco de dados
    
    Returns:
        owners (List[Owner]): lista de donos
    """
    owners = session.exec(select(Owner)).all()
    return owners
    
@router.post("/", response_model=Owner)
def create_owner(owner: Owner, session: Session = Depends(get_session)):
    """
    Docstring para create_owner
    
    Args:
        owner (Owner): objeto de dono a ser inserido
        session (Session): sessao do banco de dados

    Returns:
        owner (Owner): objeto de dono recém-inserido
    """
    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner
    
@router.get("/{owner_id}", response_model=Owner)
def list_owner(owner_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_owner
    
    Args:
        owner_id (int): id do dono a ser inserido
        session (Session): sessao do banco de dados

    Returns:
        owner (Owner): objeto de dono recém-inserido
    """
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

@router.put("/{owner_id}", response_model=Owner)
def update_owner(owner_id: int, updated_owner: Owner, session: Session = Depends(get_session)):
    """
    Docstring para update_owner
    
    Args:
        owner_id (int): id do dono a ser atualizado
        updated_owner (Owner): objeto de dono com os dados atualizados
        session (Session): sessao do banco de dados

    Returns:
        owner (Owner): objeto de dono atualizado
    """
    owner = session.get(Owner, owner_id)
    
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    owner.name = updated_owner.name
    owner.email = updated_owner.email
    session.add(owner)
    session.commit()
    session.refresh(owner)

    return owner
    
@router.delete("/{owner_id}", response_model=Owner)
def delete_owner(owner_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_owner
    
    Args:
        owner_id (int): id do dono a ser deletado
        session (Session): sessao do banco de dados

    Returns:
        owner (Owner): objeto de dono removido
    """
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    session.delete(owner)
    session.commit()
    return owner