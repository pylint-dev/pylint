from dataclasses import dataclass

from parent import AbstractParent


@dataclass
class Child(AbstractParent):
    """child class"""
    pass
