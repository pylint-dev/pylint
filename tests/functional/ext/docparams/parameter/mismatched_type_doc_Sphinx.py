"""Functional tests for mismatched-type-doc (W9022) — Sphinx style.

Expected messages are listed inline with the mismatched-type-doc marker.
The .rc file enables check-type-doc-match=yes and default-docstring-type=sphinx.
"""
# pylint: disable=missing-module-docstring,missing-return-doc,missing-return-type-doc,unused-argument,too-few-public-methods,invalid-name
from __future__ import annotations
from typing import Any, Optional


class Point:
    """A 2-D point."""


# ---------------------------------------------------------------------------
# SHOULD FIRE
# ---------------------------------------------------------------------------

def bad_sphinx_named_vs_structural(x: Point) -> int:  # [mismatched-type-doc]
    """Named class vs structural tuple in :type: tag.

    :param x: A point.
    :type x: tuple[float, float]
    :return: Result.
    :rtype: int
    """
    return 0


def bad_sphinx_int_vs_str(count: int) -> None:  # [mismatched-type-doc]
    """Primitive type mismatch.

    :param count: The count.
    :type count: str
    """


def bad_sphinx_second_param(name: str, value: int) -> None:  # [mismatched-type-doc]
    """Only the second parameter is wrong.

    :param name: The name.
    :type name: str
    :param value: The value.
    :type value: float
    """


# ---------------------------------------------------------------------------
# SHOULD NOT FIRE
# ---------------------------------------------------------------------------

def good_sphinx_exact_match(x: int, y: float) -> None:
    """Annotation and :type: tag are identical.

    :param x: An integer.
    :type x: int
    :param y: A float.
    :type y: float
    """


def good_sphinx_no_annotation(x) -> None:
    """No annotation — nothing to compare.

    :param x: A thing.
    :type x: int
    """


def good_sphinx_no_type_tag(x: int) -> None:
    """No :type: tag — different check (missing-type-doc), not W9022.

    :param x: An integer.
    """


def good_sphinx_optional_annotation(x: Optional[int]) -> None:
    """Optional annotation is an escape hatch.

    :param x: The value.
    :type x: int
    """


def good_sphinx_any_annotation(x: Any) -> None:
    """Any annotation is an escape hatch.

    :param x: The value.
    :type x: int
    """


def good_sphinx_any_in_doc(x: int) -> None:
    """Any in :type: tag is an escape hatch.

    :param x: The value.
    :type x: Any
    """


def good_sphinx_list_alias(items: list) -> None:
    """Old-style ``List`` alias normalised to ``list``.

    :param items: A list.
    :type items: List
    """


def good_sphinx_typing_prefix(items: list[int]) -> None:
    """``typing.List`` prefix stripped before comparison.

    :param items: A list.
    :type items: typing.List[int]
    """
