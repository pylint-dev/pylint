"""AttributeError: 'Subscript' object has no attribute 'name' """
# pylint: disable=missing-docstring

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from typing import Optional

from attr import attrib, attrs  # pylint: disable=import-error


@attrs()
class User:
    name: str = attrib()
    age: int = attrib()
    occupation = Optional[str] = attrib(default=None)  # [unsupported-assignment-operation]
