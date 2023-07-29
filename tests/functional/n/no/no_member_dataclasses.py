"""Test various regressions for dataclasses and no-member."""

# pylint: disable=missing-docstring, too-few-public-methods, invalid-field-call

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from abc import ABCMeta, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict


# https://github.com/pylint-dev/pylint/issues/3754
@dataclass(frozen=True)
class DeploymentState(metaclass=ABCMeta):
    type: str

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Serializes given DeploymentState instance to Dict.
        :return:
        """


@dataclass(frozen=True)
class DeploymentStateEcs(DeploymentState):
    blue: Any
    green: Any
    candidate: Any

    def to_dict(self) -> Dict:
        return {
            'type': self.type,  # No error here
            'blue': asdict(self.blue),
            'green': asdict(self.green),
            'candidate': self.candidate.value,
        }


@dataclass(frozen=True)
class DeploymentStateLambda(DeploymentState):
    current: Any
    candidate: Any

    def to_dict(self) -> Dict:
        return {
            'type': self.type,  # No error here
            'current': asdict(self.current),
            'candidate': asdict(self.candidate) if self.candidate else None,
        }


# https://github.com/pylint-dev/pylint/issues/2600
@dataclass
class TestClass:
    attr1: str
    attr2: str
    dict_prop: Dict[str, str] = field(default_factory=dict)

    def some_func(self) -> None:
        for key, value in self.dict_prop.items():  # No error here
            print(key)
            print(value)


class TestClass2:  # not a dataclass, field inferred to a Field
    attr1: str
    attr2: str
    dict_prop: Dict[str, str] = field(default_factory=dict)

    def some_func(self) -> None:
        for key, value in self.dict_prop.items():  # [no-member]
            print(key)
            print(value)


@dataclass
class TestClass3:
    attr1: str
    attr2: str
    dict_prop = field(default_factory=dict)  # No type annotation, not treated as field

    def some_func(self) -> None:
        for key, value in self.dict_prop.items():  # [no-member]
            print(key)
            print(value)
