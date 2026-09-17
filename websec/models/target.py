from dataclasses import dataclass, field


@dataclass
class Form:
    action: str
    method: str = "GET"
    inputs: list[str] = field(default_factory=list)


@dataclass
class Target:
    url: str
    method: str = "GET"
    params: dict = field(default_factory=dict)
    forms: list[Form] = field(default_factory=list)