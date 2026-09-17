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