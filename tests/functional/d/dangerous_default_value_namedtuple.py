# pylint: disable=missing-docstring, use-list-literal, use-dict-literal
import collections
from typing import List, NamedTuple


class BadListDefault(NamedTuple):
    avgs: List[float] = []  # [dangerous-default-value]
    stds: List[float] = []  # [dangerous-default-value]


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
