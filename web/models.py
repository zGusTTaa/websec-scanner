from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from web.database import Base


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    url: Mapped[str] = mapped_column(String(500))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    scans: Mapped[list["Scan"]] = relationship(
        back_populates="target", cascade="all, delete-orphan"
    )


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("targets.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")

    target: Mapped[Target] = relationship(back_populates="scans")
    findings: Mapped[list["FindingDB"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan"
    )


class FindingDB(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
    scanner: Mapped[str] = mapped_column(String(50))
    severity: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)

    scan: Mapped[Scan] = relationship(back_populates="findings")