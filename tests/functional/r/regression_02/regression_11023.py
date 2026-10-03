"""Regression test for https://github.com/pylint-dev/pylint/issues/11023.

A dataclass-synthesized ``__init__`` has no line number, which crashed
``_detect_global_scope`` while resolving a bare reference to it.
"""
from dataclasses import dataclass


@dataclass
class DataClass:
    """A dataclass referencing its own synthesized ``__init__``."""

    __init__  # [pointless-statement]
