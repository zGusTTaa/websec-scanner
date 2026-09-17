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