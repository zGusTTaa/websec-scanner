from dataclasses import dataclass, field
from datetime import datetime

from websec.models.severity import Severity


@dataclass
class Finding:
    scanner: str
    severity: Severity
    url: str
    description: str
    evidence: str = ""
    recommendation: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "scanner": self.scanner,
            "severity": self.severity.name,
            "url": self.url,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp.isoformat(),
        }