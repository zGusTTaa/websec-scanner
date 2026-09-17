from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from web import crud, schemas
from web.database import get_db

router = APIRouter(prefix="/api/targets", tags=["Targets"])


@router.get("/", response_model=list[schemas.TargetRead])
def list_targets(db: Session = Depends(get_db)):
    """Lista todos os alvos cadastrados."""
    return crud.list_targets(db)


@router.get("/{target_id}", response_model=schemas.TargetRead)
def get_target(target_id: int, db: Session = Depends(get_db)):
    """Busca um alvo pelo ID."""
    target = crud.get_target(db, target_id)
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alvo não encontrado")
    return target


@router.post("/", response_model=schemas.TargetRead, status_code=status.HTTP_201_CREATED)
def create_target(data: schemas.TargetCreate, db: Session = Depends(get_db)):
    """Cadastra um novo alvo."""
    return crud.create_target(db, data)


@router.put("/{target_id}", response_model=schemas.TargetRead)
def update_target(
    target_id: int, data: schemas.TargetUpdate, db: Session = Depends(get_db)
):
    """Atualiza um alvo existente."""
    target = crud.update_target(db, target_id, data)
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alvo não encontrado")
    return target


@router.delete("/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_target(target_id: int, db: Session = Depends(get_db)):
    """Remove um alvo e todos os scans associados."""
    if not crud.delete_target(db, target_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alvo não encontrado")