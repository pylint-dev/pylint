from dataclasses import dataclass

from namespace_inheritance.parents.parent import AbstractParent, GenericParent


@dataclass
class Child(AbstractParent):
    """Child class."""


class ConcreteChild(GenericParent[int]):
    """Child class."""
