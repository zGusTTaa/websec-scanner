from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from web import crud, schemas
from web.database import get_db
from web.services import scanner_service
from websec.scanners import SCANNER_REGISTRY

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


@router.post("/", response_model=schemas.ScanRead, status_code=status.HTTP_201_CREATED)
def create_scan(
    data: schemas.ScanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Dispara um scan em background e retorna imediatamente com status 'running'.
    O front-end deve fazer polling em GET /api/scans/{id} para acompanhar.
    """
    target = crud.get_target(db, data.target_id)
    if not target:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Alvo não encontrado")

    # Valida scanners ANTES de criar o registro no banco
    if data.scanners is not None:
        invalid = [s for s in data.scanners if s not in SCANNER_REGISTRY]
        if invalid:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Scanners inválidos: {invalid}. Disponíveis: {list(SCANNER_REGISTRY.keys())}",
            )

    scan = crud.create_scan(db, target_id=target.id)

    def run_scan_in_background(scan_id: int, target_url: str, scanners):
        """Executa o scan em uma sessão de banco separada."""
        from web.database import SessionLocal

        bg_db = SessionLocal()
        try:
            scanner_service.run_scan(
                db=bg_db,
                scan_id=scan_id,
                target_url=target_url,
                scanners=scanners,
            )
        except Exception as e:
            print(f"[background] Erro no scan {scan_id}: {e}")
        finally:
            bg_db.close()

    background_tasks.add_task(
        run_scan_in_background,
        scan.id,
        target.url,
        data.scanners,
    )

    return scan


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """Remove um scan e seus findings."""
    if not crud.delete_scan(db, scan_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Scan não encontrado")