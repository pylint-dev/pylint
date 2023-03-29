"""Regression in astroid on ClassDef inference with two test cases.
Fixed in https://github.com/pylint-dev/astroid/pull/1181"""

from typing import Tuple, Type
from typing import Dict, List, Any
from dataclasses import dataclass, field

# https://github.com/pylint-dev/pylint/issues/5030
def is_type_list(f_type: Type) -> bool:
    """just here to show the issue"""
    return f_type == list

assert not is_type_list(Tuple)


# https://github.com/pylint-dev/pylint/issues/5036
@dataclass
class SomeData:
    """A dataclass."""
    a_dict: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class SubSomeData(SomeData):
    """A subclass of a dataclass."""

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Subclass init func."""
        super().__init__(**kwargs)
        if "test" in self.a_dict:
            print(self.a_dict["test"])
