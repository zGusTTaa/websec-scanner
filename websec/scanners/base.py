from abc import ABC, abstractmethod

from websec.core.session import Session
from websec.models.finding import Finding
from websec.models.target import Target


class BaseScanner(ABC):
    name: str = "base"
    description: str = ""

    def __init__(self, session: Session, config: dict | None = None):
        self.session = session
        self.config = config or {}

    @abstractmethod
    def scan(self, target: Target) -> list[Finding]:
        ...