"""Unpack values returned by functions that are only declared in a stub."""
# Several fixtures below return ``None`` on purpose: the point is what the
# checker can infer from the *annotation*, not that assigning from a
# ``None``-returning call is itself a smell.
# pylint: disable=assignment-from-none
from pyi_stub_unpacking import (
    declared_class,
    declared_int,
    declared_none,
    declared_tuple,
    declared_unresolved,
    declared_without_annotation,
)

FIRST, SECOND, THIRD = declared_tuple()
VALUE, _REST = declared_int()
# The annotation names the class of the returned value: it is instantiated, so
# an iterable class unpacks cleanly.
LEFT, RIGHT = declared_class()
# An unresolved forward reference keeps the previous behaviour: nothing can be
# inferred, so the checker says nothing rather than guessing.
ALSO_LEFT, ALSO_RIGHT = declared_unresolved()
# A stub that declares no return type, and one that declares ``None``: there is
# no annotation to use, so both keep the old behaviour.
NONE_LEFT, NONE_RIGHT = declared_without_annotation()
EXPLICIT_LEFT, EXPLICIT_RIGHT = declared_none()


def annotated_none() -> None:
    """A real function, not a stub: the body is what returns ``None``."""
    return


# A real function, not a stub: its body says what it returns, so the checker
# leaves it alone.
REAL_LEFT, REAL_RIGHT = annotated_none()
