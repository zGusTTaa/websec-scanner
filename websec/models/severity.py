from enum import Enum


class Severity(Enum):
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

    @property
    def label(self) -> str:
        return self.name.capitalize()

    @property
    def color(self) -> str:
        return {
            "INFO": "blue",
            "LOW": "green",
            "MEDIUM": "yellow",
            "HIGH": "orange3",
            "CRITICAL": "red",
        }[self.name]