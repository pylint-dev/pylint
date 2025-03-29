# Test for https://github.com/pylint-dev/pylint/issues/10236

class Component:
    """A component class."""
    def __init__(self, name: str):
        self.name = name


class Container:
    """A container class that uses comprehension to create components."""
    def __init__(self):
        self.components = [Component(f"component_{i}") for i in range(3)] # list
        self.component_dict = {i: Component(f"dict_component_{i}") for i in range(2)} # dict
        self.components_set = {Component(f"set_component_{i}") for i in range(2)} # set
        self.lazy_components = (Component(f"lazy_{i}") for i in range(2)) # generator


class MultiContainer:
    """A container with multiple component types."""
    def __init__(self):
        # Test mixed component types in a list
        self.mixed = [Component("first"), Container()]
