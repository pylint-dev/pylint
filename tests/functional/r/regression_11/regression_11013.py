"""Regression test for #11013: TypeAlias imported from typing_extensions.

``typing_extensions.TypeAlias`` infers to both a ``ClassDef`` (via the typing
brain remap) and a ``FunctionDef`` (the legacy typing_extensions implementation).
``safe_infer`` returned ``None`` for the ambiguous result, so the assignment was
not recognised as a type alias and pylint fell through to the ``invalid-name``
``const`` check.
"""
# pylint: disable=missing-class-docstring,unused-import,too-few-public-methods
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    AuthenticationType: TypeAlias = "Authentication"


class Authentication: ...
