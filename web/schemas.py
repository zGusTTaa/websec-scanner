from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------- Target ----------
class TargetBase(BaseModel):
    name: str
    url: str
    notes: str | None = None


class TargetCreate(TargetBase):
    """Payload para criar um novo alvo."""
    pass


class TargetUpdate(BaseModel):
    """Payload para atualizar — todos os campos opcionais."""
    name: str | None = None
    url: str | None = None
    notes: str | None = None


class TargetRead(TargetBase):
    """O que a API devolve."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # ---------- Scan ----------
class ScanCreate(BaseModel):
    """Payload para disparar um scan."""
    target_id: int
    scanners: list[str] | None = None  # ex: ["headers", "server_info"]; None = todos


class ScanRead(BaseModel):
    id: int
    target_id: int
    started_at: datetime
    finished_at: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ScanDetail(ScanRead):
    """Scan com contagem de findings por severidade."""
    total_findings: int = 0
    findings: list["FindingRead"] = []


# ---------- Finding ----------
class FindingRead(BaseModel):
    id: int
    scan_id: int
    scanner: str
    severity: str
    url: str
    description: str
    evidence: str | None = None
    recommendation: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Reativar referência futura (ScanDetail usa FindingRead)
ScanDetail.model_rebuild()