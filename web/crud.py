from sqlalchemy.orm import Session

from web import models, schemas


# ---------- Target ----------
def list_targets(db: Session) -> list[models.Target]:
    return db.query(models.Target).order_by(models.Target.created_at.desc()).all()


def get_target(db: Session, target_id: int) -> models.Target | None:
    return db.get(models.Target, target_id)


def create_target(db: Session, data: schemas.TargetCreate) -> models.Target:
    target = models.Target(**data.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


def update_target(
    db: Session, target_id: int, data: schemas.TargetUpdate
) -> models.Target | None:
    target = db.get(models.Target, target_id)
    if not target:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(target, field, value)
    db.commit()
    db.refresh(target)
    return target


def delete_target(db: Session, target_id: int) -> bool:
    target = db.get(models.Target, target_id)
    if not target:
        return False
    db.delete(target)
    db.commit()
    return True
from datetime import datetime

from web import models, schemas
from websec.models.severity import Severity


# ---------- Scan ----------
def list_scans(db: Session, target_id: int | None = None) -> list[models.Scan]:
    query = db.query(models.Scan)
    if target_id is not None:
        query = query.filter(models.Scan.target_id == target_id)
    return query.order_by(models.Scan.started_at.desc()).all()


def get_scan(db: Session, scan_id: int) -> models.Scan | None:
    return db.get(models.Scan, scan_id)


def create_scan(db: Session, target_id: int) -> models.Scan:
    scan = models.Scan(target_id=target_id, status="running")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def finish_scan(db: Session, scan_id: int, status: str = "completed") -> None:
    scan = db.get(models.Scan, scan_id)
    if scan:
        scan.status = status
        scan.finished_at = datetime.utcnow()
        db.commit()


def delete_scan(db: Session, scan_id: int) -> bool:
    scan = db.get(models.Scan, scan_id)
    if not scan:
        return False
    db.delete(scan)
    db.commit()
    return True


def save_finding(
    db: Session, scan_id: int, finding  # websec.models.finding.Finding
) -> models.FindingDB:
    """Converte o Finding do motor para FindingDB e persiste."""
    db_finding = models.FindingDB(
        scan_id=scan_id,
        scanner=finding.scanner,
        severity=finding.severity.name,  # Enum → string
        url=finding.url,
        description=finding.description,
        evidence=finding.evidence or "",
        recommendation=finding.recommendation or "",
    )
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding


# ---------- Finding ----------
def list_findings(
    db: Session,
    scan_id: int | None = None,
    severity: str | None = None,
) -> list[models.FindingDB]:
    query = db.query(models.FindingDB)
    if scan_id is not None:
        query = query.filter(models.FindingDB.scan_id == scan_id)
    if severity is not None:
        query = query.filter(models.FindingDB.severity == severity.upper())
    return query.all()


def get_finding(db: Session, finding_id: int) -> models.FindingDB | None:
    return db.get(models.FindingDB, finding_id)


def delete_finding(db: Session, finding_id: int) -> bool:
    finding = db.get(models.FindingDB, finding_id)
    if not finding:
        return False
    db.delete(finding)
    db.commit()
    return True