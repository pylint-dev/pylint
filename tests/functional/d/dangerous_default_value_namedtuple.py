# pylint: disable=missing-module-docstring, missing-class-docstring, use-list-literal, use-dict-literal
import collections
import random
from typing import NamedTuple

DANGEROUS_GLOBAL = set()

AMBIGUOUS_DEFAULT = [] if random.random() > 0.5 else {}


class BadListDefault(NamedTuple):
    avgs: list[float] = []  # [dangerous-default-value]
    stds: list[float] = []  # [dangerous-default-value]


class BadDictDefault(NamedTuple):
    data: dict = {}  # [dangerous-default-value]


class BadSetDefault(NamedTuple):
    items: set = set()  # [dangerous-default-value]


class BadSetLiteralDefault(NamedTuple):
    items: set = {1, 2}  # [dangerous-default-value]


class BadListCallDefault(NamedTuple):
    items: list = list()  # [dangerous-default-value]


class BadDictCallDefault(NamedTuple):
    data: dict = dict()  # [dangerous-default-value]


class BadDequeDefault(NamedTuple):
    items: collections.deque = collections.deque()  # [dangerous-default-value]


class SafeNamedTuple(NamedTuple):
    name: str = "default"
    count: int = 0
    flag: bool = True
    tags: tuple = ()
    frozen: frozenset = frozenset()


class MixedNamedTuple(NamedTuple):
    name: str = "ok"
    items: list = []  # [dangerous-default-value]


class NoDefaultNamedTuple(NamedTuple):
    name: str
    value: int


class GlobalDangerousDefault(NamedTuple):
    items: set = DANGEROUS_GLOBAL  # [dangerous-default-value]


class UninferrableDefault(NamedTuple):
    items: list | dict = AMBIGUOUS_DEFAULT
