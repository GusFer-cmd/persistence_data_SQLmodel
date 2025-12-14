from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.models import CollectionCarLink

router = APIRouter(prefix="/collection_car_links", tags=["Collection Car Links"])

#collection car links
@router.get("/", response_model=list[CollectionCarLink])
def list_collection_car_links(session: Session = Depends(get_session)):
    """
    Docstring para list_collection_car_links
    
    Args:
        session (Session): sessao do banco

    Return:
        links (List[CollectionCarLink]): lista com associacoes entre colecoes e carros
    """
    links = session.exec(select(CollectionCarLink)).all()
    return links
    
@router.post("/", response_model=CollectionCarLink)
def create_collection_car_link(link: CollectionCarLink, session: Session = Depends(get_session)):
    """
    Docstring para create_collection_car_link
    
    Args:
        link (CollectionCarLink): objeto da associacao entre carro e colecao
        session (Session): sessao do banco de dados
    
    Returns:
        link (CollectionCarLink): objeto da associacao entre carro e colecao inserido na tabela
    """
    session.add(link)
    session.commit()
    session.refresh(link)
    return link
    
@router.delete("/{collection_item_id}/{car_id}", response_model=CollectionCarLink)
def delete_collection_car_link(collection_item_id: int, car_id: int, session: Session = Depends(get_session)):
    """
    Docstring para delete_collection_car_link
    
    Args:
        collection_item_id (int): id da colecao
        car_id (int): id do carro
        session (Session): sessao do banco de dados
    
    Returns:
        link (CollectionCarLink): objeto da associacao entre carro e colecao removido na tabela
    """
    link = session.get(CollectionCarLink, (collection_item_id, car_id))
    if not link:
        raise HTTPException(status_code=404, detail="Collection Car Link not found")
    session.delete(link)
    session.commit()
    return link
