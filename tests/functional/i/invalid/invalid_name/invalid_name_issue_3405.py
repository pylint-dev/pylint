""" Regression test for https://github.com/pylint-dev/pylint/issues/3405. """

import dataclasses
from typing import ClassVar


@dataclasses.dataclass
class Foo:
    """ClassVar attribute should be matched against class-attribute-rgx, not attr-rgx"""
    # class-attribute-rgx='^y$'
    x: ClassVar[int] = 0  # [invalid-name]
