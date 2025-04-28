# pylint: disable=R0903, W0107

"""Test invalid return type overrides in method inheritance."""

from abc import ABC, abstractmethod
from io import TextIOWrapper, BytesIO

# Case 1: Simple type mismatch
class Parent:
    """Parent class with a method returning int."""
    def method(self) -> int:
        """Returns an integer value."""
        return 42

class Child(Parent):
    """Child class overriding method to return a string."""
    def method(self) -> str:  # [invalid-overridden-method]
        """Overrides method to return a string."""
        return "hello"

# Case 2: None vs concrete type
class ParentNone:
    """Parent class with a method returning None."""
    def method(self) -> None:
        """Method returns None."""
        raise NotImplementedError("This method should be overridden")

class ChildNone(ParentNone):
    """Child class overriding method to return an int."""
    def method(self) -> int:  # [invalid-overridden-method]
        """Overrides method to return an integer."""
        return 42

# Case 5: Abstract base class with different return type
class BaseClass(ABC):
    """Abstract base class with an abstract method returning TextIOWrapper."""
    @abstractmethod
    def read_file(self, path: str) -> TextIOWrapper:
        """Abstract method that should return a TextIOWrapper."""
        raise NotImplementedError("Method must be implemented by subclass")

class ChildClass(BaseClass):
    """Child class overriding read_file method returning BytesIO."""
    def read_file(self, path: str) -> BytesIO:  # [invalid-overridden-method]
        """Implementation returns BytesIO instead of TextIOWrapper."""
        return BytesIO(b"content")

# Case 6: Method returns a subtype of the expected return type (valid override)
class Animal:
    """Base class with a method returning a generic Animal."""
    def make_sound(self) -> 'Animal':
        """Returns an Animal instance."""
        return self

class Dog(Animal):
    """Dog class overrides make_sound method returning a Dog."""
    def make_sound(self) -> 'Dog':  # This is valid as Dog is a subtype of Animal
        """Returns a Dog instance."""
        return self

# Case 8: Overriding method with more specific return type annotation
class FileReader:
    """Class for reading files."""
    def get_contents(self) -> 'Any':
        """Returns contents of the file."""
        return "file contents"

class JSONReader(FileReader):
    """Class for reading JSON files."""
    def get_contents(self) -> dict:  # [invalid-overridden-method]
        """Overrides to return a dictionary."""
        return {"key": "value"}

# Case 9: Abstract method with invalid return type in subclass
class AbstractClass(ABC):
    """Abstract class with an abstract method."""
    @abstractmethod
    def get_value(self) -> float:
        """Returns a float value."""
        pass

class ConcreteClass(AbstractClass):
    """Concrete class with an invalid override."""
    def get_value(self) -> str:  # [invalid-overridden-method]
        """Returns a string instead of a float."""
        return "not a float"
