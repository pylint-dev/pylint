# pylint: disable=missing-module-docstring, missing-class-docstring, use-list-literal, use-dict-literal
import collections
from typing import NamedTuple

DANGEROUS_GLOBAL = set()


class CustomMutableStore(dict): pass
class CustomImmutableStore(frozenset): pass

def create_my_custom_immutable_data_store() -> CustomImmutableStore:
    return CustomImmutableStore()
    
    
def create_my_custom_mutable_data_store() -> CustomMutableStore:
    return CustomMutableStore()

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
