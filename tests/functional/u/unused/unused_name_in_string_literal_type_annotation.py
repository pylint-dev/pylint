"""Test if pylint sees names inside string literal type annotations. #3299"""
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import TypeAlias

def unused_variable_should_not_be_emitted():
    """unused-variable shouldn't be emitted for Example1."""
    Example1: TypeAlias = int
    result: set["Example1"] = set()
    return result

# unused-import shouldn't be emitted for Path
example2: set["Path"] = set()

def example3(_: "ArgumentParser"):
    """unused-import shouldn't be emitted for ArgumentParser"""

# pylint: disable=too-few-public-methods
class Class:
    """unused-import shouldn't be emitted for Namespace"""
    cls: "Namespace"
