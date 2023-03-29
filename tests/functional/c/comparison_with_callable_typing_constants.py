"""Typing constants are actually implemented as functions, but they
raise when called, so Pylint uses that to avoid false positives for
comparison-with-callable.
"""
from typing import Any, Optional


def check_any(type_) -> bool:
    """See https://github.com/pylint-dev/pylint/issues/5557"""
    return type_ == Any


def check_optional(type_) -> bool:
    """
    Unlike Any, Optional does not raise in its body.
    It raises via its decorator: typing._SpecialForm.__call__()
    """
    return type_ == Optional
