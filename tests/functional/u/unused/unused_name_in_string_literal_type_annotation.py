"""Test if pylint sees names inside string literal type annotations. #3299"""
# pylint: disable=too-few-public-methods

from argparse import ArgumentParser, Namespace
import os
from os import PathLike
from pathlib import Path
from typing import NoReturn, Set

# unused-import shouldn't be emitted for Path
example1: Set["Path"] = set()

def example2(_: "ArgumentParser") -> "NoReturn":
    """unused-import shouldn't be emitted for ArgumentParser or NoReturn."""
    while True:
        pass

def example3(_: "os.PathLike[str]") -> None:
    """unused-import shouldn't be emitted for os."""

def example4(_: "PathLike[str]") -> None:
    """unused-import shouldn't be emitted for PathLike."""

# pylint shouldn't crash with the following strings in a type annotation context
example5: Set[""]
example6: Set[" "]
example7: Set["?"]

class Class:
    """unused-import shouldn't be emitted for Namespace"""
    cls: "Namespace"
