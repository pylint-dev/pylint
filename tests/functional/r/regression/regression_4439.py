"""AttributeError: 'Subscript' object has no attribute 'name' """
# pylint: disable=missing-docstring

from typing import Optional

from attr import attrib, attrs


@attrs()
class User:
    name: str = attrib()
    age: int = attrib()
    occupation = Optional[str] = attrib(default=None) # [unsupported-assignment-operation]
