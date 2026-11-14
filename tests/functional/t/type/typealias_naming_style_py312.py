"""PEP 695 generic typing nodes"""

from typing import TypeAliasType

type Point[T] = tuple[T, ...]
type point[T] = tuple[T, ...]  # [invalid-name]

# Names bound to an existing type alias are type aliases too
PointAlias = Point
point_alias = Point  # [invalid-name]
Vector = TypeAliasType("Vector", list[float])
vector = TypeAliasType("vector", list[float])  # [invalid-name]


# Variables annotated with a type alias are not type aliases
MODULE_POINT: Point[int] | None = None


def function_with_annotated_variable():
    """Annotated local variables follow the variable naming style."""
    local_point: Point[int] | None = None
    other_point: Point[int] = (1, 2)
    return local_point, other_point
