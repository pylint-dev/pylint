# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, too-few-public-methods, use-list-literal
import collections
import dataclasses
import typing
from dataclasses import InitVar, dataclass, field
from typing import ClassVar

DANGEROUS_GLOBAL = set()


@dataclass
class BadDefaults:
    items: list = []  # [dangerous-default-value]
    data: dict = {}  # [dangerous-default-value]
    tags: set = {1, 2}  # [dangerous-default-value]
    called: list = list()  # [dangerous-default-value]
    queue: collections.deque = collections.deque()  # [dangerous-default-value]
    shared: set = DANGEROUS_GLOBAL  # [dangerous-default-value]


@dataclass
class BadFieldDefaults:
    items: list = field(default=[])  # [dangerous-default-value]
    data: dict = dataclasses.field(default={})  # [dangerous-default-value]


@dataclass
class BadInitVar:
    seed: InitVar[list] = []  # [dangerous-default-value]


@dataclass(frozen=True)
class BadFrozen:
    items: list = []  # [dangerous-default-value]


@dataclass
class SafeDefaults:
    required: list = field()
    name: str = "default"
    count: int = 0
    frozen: frozenset = frozenset()
    items: list = field(default_factory=list)
    data: dict = dataclasses.field(default_factory=dict)
    number: int = field(default=0)
    shared: ClassVar[list] = []
    registry: typing.ClassVar[dict] = {}
    plain = []


class NotADataclass:
    items: list = []
