# Test for https://github.com/pylint-dev/pylint/issues/10236
from collections.abc import Generator


class Component:
    """A component class."""
    def __init__(self, name: str):
        self.name = name


class Container:
    """A container class that uses comprehension to create components."""
    def __init__(self):
        self.components: list[Component] = [Component(f"component_{i}") for i in range(3)] # list
        self.component_dict: dict[int, Component] = {i: Component(f"dict_component_{i}") for i in range(2)} # dict
        self.components_set: set[Component] = {Component(f"set_component_{i}") for i in range(2)} # set
        self.lazy_components: Generator[Component] = (Component(f"lazy_{i}") for i in range(2)) # generator
