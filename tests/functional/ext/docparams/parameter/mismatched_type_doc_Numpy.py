"""Functional tests for mismatched-type-doc (W9022) — NumPy style.

Expected messages are listed inline with the mismatched-type-doc marker.
The .rc file enables check-type-doc-match=yes and default-docstring-type=numpy.
"""
# pylint: disable=missing-module-docstring,missing-return-doc,missing-return-type-doc,unused-argument,too-few-public-methods,invalid-name
from __future__ import annotations
from typing import Any, Optional


class Point:
    """A 2-D point."""


# ---------------------------------------------------------------------------
# SHOULD FIRE
# ---------------------------------------------------------------------------

def bad_numpy_named_vs_structural(x: Point) -> int:  # [mismatched-type-doc]
    """Named class vs structural tuple.

    Parameters
    ----------
    x : tuple[float, float]
        A point.

    Returns
    -------
    int
        Result.
    """
    return 0


def bad_numpy_int_vs_str(count: int) -> None:  # [mismatched-type-doc]
    """Primitive type mismatch.

    Parameters
    ----------
    count : str
        The count.
    """


def bad_numpy_second_param(name: str, value: int) -> None:  # [mismatched-type-doc]
    """Only the second parameter is wrong; first is correct.

    Parameters
    ----------
    name : str
        The name — matches annotation.
    value : float
        The value — annotation says int.
    """


# ---------------------------------------------------------------------------
# SHOULD NOT FIRE
# ---------------------------------------------------------------------------

def good_numpy_exact_match(x: int, y: float) -> None:
    """Annotation and docstring type are identical.

    Parameters
    ----------
    x : int
        An integer.
    y : float
        A float.
    """


def good_numpy_no_annotation(x) -> None:
    """No annotation — nothing to compare against.

    Parameters
    ----------
    x : int
        A thing.
    """


def good_numpy_no_doc_type(x: int) -> None:
    """No type in docstring — missing-type-doc territory, not W9022.

    Parameters
    ----------
    x
        A thing without a type line.
    """


def good_numpy_optional_annotation(x: Optional[int]) -> None:
    """Optional annotation is an escape hatch.

    Parameters
    ----------
    x : int
        The value.
    """


def good_numpy_union_annotation(x: int | str) -> None:
    """Union annotation is an escape hatch.

    Parameters
    ----------
    x : int
        The value.
    """


def good_numpy_any_annotation(x: Any) -> None:
    """Any annotation is an escape hatch.

    Parameters
    ----------
    x : int
        The value.
    """


def good_numpy_any_in_doc(x: int) -> None:
    """Any in docstring type is an escape hatch.

    Parameters
    ----------
    x : Any
        The value.
    """


def good_numpy_list_alias(items: list) -> None:
    """Old-style ``List`` alias normalised to ``list``.

    Parameters
    ----------
    items : List
        A list.
    """


def good_numpy_optional_type_string(x: int) -> None:
    """NumPy 'str, optional' pattern — escape hatch via Optional keyword.

    Parameters
    ----------
    x : int, optional
        An optional int with default.
    """


def good_numpy_typing_prefix(items: list[int]) -> None:
    """``typing.List`` prefix stripped before comparison.

    Parameters
    ----------
    items : typing.List[int]
        A list of ints.
    """
