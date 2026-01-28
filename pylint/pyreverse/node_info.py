# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Dataclass wrappers for storing analysis info about astroid nodes.

This module provides typed dataclasses to hold the analysis metadata that was
previously stored directly on astroid nodes. This enables proper type hints
and avoids modifying external objects.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from astroid import nodes


K = TypeVar("K")
V = TypeVar("V")


class InfoDict(dict[K, V], Generic[K, V]):
    """Dict that auto-creates values using a factory when accessing missing keys."""

    def __init__(self, factory: type[V]) -> None:
        super().__init__()
        self._factory = factory

    def __missing__(self, key: K) -> V:
        self[key] = self._factory()
        return self[key]


@dataclass
class ModuleInfo:
    """Analysis info for Module nodes.

    Attributes:
        locals_type: Mapping from local names to inferred types.
        depends: List of module dependencies.
        type_depends: List of type-checking-only dependencies.
        uid: Unique identifier (only set if Linker tag=True).
    """

    locals_type: defaultdict[str, list[nodes.NodeNG]] = field(
        default_factory=lambda: defaultdict(list)
    )
    depends: list[str] = field(default_factory=list)
    type_depends: list[str] = field(default_factory=list)
    uid: int | None = None


@dataclass
class ClassInfo:
    """Analysis info for ClassDef nodes.

    Attributes:
        locals_type: Mapping from local names to inferred types.
        instance_attrs_type: Mapping from instance attribute names to types.
        compositions_type: Attributes representing composition relationships.
        aggregations_type: Attributes representing aggregation relationships.
        associations_type: Attributes representing association relationships.
        specializations: List of subclasses.
        uid: Unique identifier (only set if Linker tag=True).
    """

    locals_type: defaultdict[str, list[nodes.NodeNG]] = field(
        default_factory=lambda: defaultdict(list)
    )
    instance_attrs_type: defaultdict[str, list[nodes.NodeNG]] = field(
        default_factory=lambda: defaultdict(list)
    )
    compositions_type: defaultdict[str, list[nodes.ClassDef]] = field(
        default_factory=lambda: defaultdict(list)
    )
    aggregations_type: defaultdict[str, list[nodes.ClassDef]] = field(
        default_factory=lambda: defaultdict(list)
    )
    associations_type: defaultdict[str, list[nodes.ClassDef]] = field(
        default_factory=lambda: defaultdict(list)
    )
    specializations: list[nodes.ClassDef] = field(default_factory=list)
    uid: int | None = None


@dataclass
class FunctionInfo:
    """Analysis info for FunctionDef nodes.

    Attributes:
        locals_type: Mapping from local names to inferred types.
        uid: Unique identifier (only set if Linker tag=True).
    """

    locals_type: defaultdict[str, list[nodes.NodeNG]] = field(
        default_factory=lambda: defaultdict(list)
    )
    uid: int | None = None
