from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from web import crud, schemas
from web.database import get_db

router = APIRouter(prefix="/api/findings", tags=["Findings"])


@router.get("/", response_model=list[schemas.FindingRead])
def list_findings(
    scan_id: int | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
):
    """Lista findings, filtrando por scan e/ou severidade."""
    return crud.list_findings(db, scan_id=scan_id, severity=severity)


@router.get("/{finding_id}", response_model=schemas.FindingRead)
def get_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud.get_finding(db, finding_id)
    if not finding:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding não encontrado")
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finding(finding_id: int, db: Session = Depends(get_db)):
    if not crud.delete_finding(db, finding_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding não encontrado")