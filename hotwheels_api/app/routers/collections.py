from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import Collection

router = APIRouter(prefix="/collection", tags=["Collection"])

#collection items
@router.get("/", response_model=list[Collection])
def list_collection_items(session: Session = Depends(get_session)):
    """
    Docstring para list_collection_items
    
    Args:
        session (Session): sessao do banco
    
    Returns:
        items (List[Collection]): lista com todas as colecoes
    """
    items = session.exec(select(Collection)).all()
    return items

@router.get("/paged", response_model=list[Collection])
def list_collections_items_paged(offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)):
    """
    Docstring para list_collections_paged
    
    Args:
        offset (int): deslocamento inicial
        limit (int): limite de registros a serem retornados
        session (Session): sessao do banco
    
    Returns:
        collection (List[Collection]): lista com as colecoes dentro do intervalo fornecido
    """
    collection = session.exec(select(Collection).offset(offset).limit(limit)).all()
    return collection

@router.post("/", response_model=Collection)
def create_collection_item(item: Collection, session: Session = Depends(get_session)):
    """
    Docstring para create_collection_item
    
    Args:
        item (Collection): colecao a ser adicionada
        session (Session): sessao do banco
    
    Returns:
        item (Collection): colecao adicionada no banco
    """
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
    
@router.get("/{item_id}", response_model=Collection)
def list_collection_item(item_id: int, session: Session = Depends(get_session)):
    """
    Docstring para list_collection_item
    
    Args:
        item_id (int): id da colecao
        session (Session): sessao do banco

    Returns:
        item (Collection): colecao com o id fornecido
    """
    item = session.get(Collection, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Collection Item not found")
    return item
    
@router.delete("/{item_id}", response_model=Collection)
def delete_collection_item(item_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_collection_item
    
    Args:
        item_id (int): id da colecao
        session (Session): sessao do banco

    Returns:
        item (Collection): colecao deletada com o id correspondente
    """
    item = session.get(Collection, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Collection Item not found")
    session.delete(item)
    session.commit()
    return item