# pylint: disable=invalid-field-call
"""Various regression tests for dataclasses."""
# See issues:
# - https://github.com/pylint-dev/pylint/issues/2605
# - https://github.com/pylint-dev/pylint/issues/2698
from dataclasses import dataclass, field
import dataclasses as dc
from typing import cast


@dataclass
class Test:
    """A test dataclass with a field, that has a default_factory."""

    test: list = field(default_factory=list)


TEST = Test()
TEST.test.append(1)
print(TEST.test[0])


@dc.dataclass  # Note the use of dc instead of dataclasses
class Test2:
    """Test dataclass that uses a renamed import of dataclasses"""
    int_prop: int = dc.field(default=10)
    list_prop: list = dc.field(default_factory=list)
    dict_prop: dict = dc.field(default_factory=dict)


TEST2 = Test2()
for _ in TEST2.list_prop:  # This is okay
    pass


TEST2.dict_prop["key"] = "value"  # This is okay


# Test2.int_prop is inferred as 10, not a Field
print(Test2.int_prop + 1)
for _ in Test2.int_prop:  # [not-an-iterable]
    pass


Test2.int_prop["key"] = "value"  # [unsupported-assignment-operation]


@dc.dataclass
class TEST3:
    """Test dataclass that puts call to field() in another function call"""
    attribute: int = cast(int, field(default_factory=dict))


@dc.dataclass
class TEST4:
    """Absurd example to test a potential crash found during development."""
    attribute: int = lambda this: cast(int, this)(field(default_factory=dict))
