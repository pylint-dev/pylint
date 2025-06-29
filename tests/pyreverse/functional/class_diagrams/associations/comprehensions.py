# Test for https://github.com/pylint-dev/pylint/issues/10236
from collections.abc import Generator
from dataclasses import dataclass


class Component:
    """A component class."""
    def __init__(self, name: str):
        self.name = name

class AssociationContainer:
    """Type hints only - no ownership."""
    def __init__(self):
        # Association: just type hints, no actual assignment
        self.components: list[Component]
        self.component_dict: dict[int, Component]
        self.components_set: set[Component]
        self.lazy_components: Generator[Component]

class CompositionContainer:
    """Comprehensions creating new objects - composition."""
    def __init__(self):
        # Composition: comprehensions creating new objects
        self.components: list[Component] = [Component(f"component_{i}") for i in range(3)]
        self.component_dict: dict[int, Component] = {i: Component(f"dict_component_{i}") for i in range(2)}
        self.components_set: set[Component] = {Component(f"set_component_{i}") for i in range(2)}
        self.lazy_components: Generator[Component] = (Component(f"lazy_{i}") for i in range(2))
