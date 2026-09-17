from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from web import crud, schemas
from web.database import get_db
from web.services import scanner_service

router = APIRouter(prefix="/api/scans", tags=["Scans"])


@router.get("/", response_model=list[schemas.ScanRead])
def list_scans(target_id: int | None = None, db: Session = Depends(get_db)):
    """Lista scans, opcionalmente filtrando por alvo."""
    return crud.list_scans(db, target_id=target_id)


@router.get("/{scan_id}", response_model=schemas.ScanDetail)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """Detalhes de um scan, incluindo findings."""
    scan = crud.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scan não encontrado")

    findings = crud.list_findings(db, scan_id=scan_id)
    return schemas.ScanDetail(
        id=scan.id,
        target_id=scan.target_id,
        started_at=scan.started_at,
        finished_at=scan.finished_at,
        status=scan.status,
        total_findings=len(findings),
        findings=[schemas.FindingRead.model_validate(f) for f in findings],
    )


@router.post("/", response_model=schemas.ScanDetail, status_code=status.HTTP_201_CREATED)
def create_scan(data: schemas.ScanCreate, db: Session = Depends(get_db)):
    """Dispara um scan em um alvo cadastrado."""
    target = crud.get_target(db, data.target_id)
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alvo não encontrado")

    scan = crud.create_scan(db, target_id=target.id)

    try:
        scanner_service.run_scan(
            db=db,
            scan_id=scan.id,
            target_url=target.url,
            scanners=data.scanners,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    # Recarrega do banco (agora com findings e status final)
    db.refresh(scan)
    findings = crud.list_findings(db, scan_id=scan.id)

    return schemas.ScanDetail(
        id=scan.id,
        target_id=scan.target_id,
        started_at=scan.started_at,
        finished_at=scan.finished_at,
        status=scan.status,
        total_findings=len(findings),
        findings=[schemas.FindingRead.model_validate(f) for f in findings],
    )


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """Remove um scan e seus findings."""
    if not crud.delete_scan(db, scan_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scan não encontrado")