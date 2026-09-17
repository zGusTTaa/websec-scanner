"""Modelos de dados do scanner."""

from websec.models.finding import Finding
from websec.models.severity import Severity
from websec.models.target import Form, Target

__all__ = ["Finding", "Severity", "Form", "Target"]