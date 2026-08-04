"""Functional tests for mismatched-type-doc (W9022) — Google style.

Expected messages are listed inline with the mismatched-type-doc marker.
The .rc file enables check-type-doc-match=yes and default-docstring-type=google.
"""
# pylint: disable=missing-module-docstring,missing-return-doc,missing-return-type-doc,unused-argument,too-few-public-methods,invalid-name
from __future__ import annotations
from typing import Any, Optional


class Point:
    """A 2-D point."""


# ---------------------------------------------------------------------------
# SHOULD FIRE — clear type mismatch
# ---------------------------------------------------------------------------

def bad_google_named_vs_structural(x: Point) -> int:  # [mismatched-type-doc]
    """Named class vs structural tuple in docstring.

    Args:
        x (tuple[float, float]): A point.

    Returns:
        int: Result.
    """
    return 0


def bad_google_int_vs_str(count: int) -> None:  # [mismatched-type-doc]
    """Primitive type mismatch.

    Args:
        count (str): The count.
    """


def bad_google_second_param(name: str, value: int) -> None:  # [mismatched-type-doc]
    """Only the second parameter is wrong; first is correct.

    Args:
        name (str): The name — matches annotation.
        value (float): The value — annotation says int.
    """


# ---------------------------------------------------------------------------
# SHOULD NOT FIRE
# ---------------------------------------------------------------------------

def good_google_exact_match(x: int, y: float) -> None:
    """Annotation and docstring type are identical.

    Args:
        x (int): An integer.
        y (float): A float.
    """


def good_google_no_annotation(x) -> None:
    """No annotation — nothing to compare against.

    Args:
        x (int): Documented type, but no annotation to check.
    """


def good_google_no_doc_type(x: int) -> None:
    """No type in docstring — different check (missing-type-doc), not W9022.

    Args:
        x: An integer with no type in docstring.
    """


def good_google_optional_annotation(x: Optional[int]) -> None:
    """Optional annotation is an escape hatch — no W9022.

    Args:
        x (int): The value.
    """


def good_google_union_annotation(x: int | str) -> None:
    """Union annotation is an escape hatch — no W9022.

    Args:
        x (int): The value.
    """


def good_google_any_annotation(x: Any) -> None:
    """Any annotation is an escape hatch — no W9022.

    Args:
        x (int): The value.
    """


def good_google_any_in_doc(x: int) -> None:
    """Any in docstring is an escape hatch — no W9022.

    Args:
        x (Any): The value.
    """


def good_google_list_alias(items: list) -> None:
    """Old-style ``List`` alias matches modern ``list`` after normalisation.

    Args:
        items (List): A list.
    """


def good_google_tuple_alias(coords: tuple) -> None:
    """Old-style ``Tuple`` alias normalised to ``tuple``.

    Args:
        coords (Tuple): Coordinates.
    """


def good_google_typing_prefix(items: list[int]) -> None:
    """``typing.List`` prefix is stripped before comparison.

    Args:
        items (typing.List[int]): A list of ints.
    """
