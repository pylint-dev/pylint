"""A test script the confuses pylint."""
# https://github.com/PyCQA/pylint/issues/2605
from dataclasses import dataclass, field


@dataclass
class Test:
    """A test dataclass with a field, that has a default_factory."""

    test: list = field(default_factory=list)


TEST = Test()
TEST.test.append(1)
print(TEST.test[0])
