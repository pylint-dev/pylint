# pylint: disable=missing-module-docstring, missing-class-docstring
from dataclasses import dataclass, fields

try:
    from dataclasses import field
except ImportError:
    field = None


@dataclass
class Settings:
    items: list = field(default_factory=list)
    data: dict = field(default_factory=dict)
    bad: list = field(default=[])  # [dangerous-default-value]


for field in fields(Settings):
    print(field.name)
