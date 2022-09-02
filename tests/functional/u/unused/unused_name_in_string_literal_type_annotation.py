"""Test if pylint sees names inside string literal type annotations. #3299"""
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Set

# unused-import shouldn't be emitted for Path
example1: Set["Path"] = set()

def example2(_: "ArgumentParser"):
    """unused-import shouldn't be emitted for ArgumentParser"""

# pylint: disable=too-few-public-methods
class Class:
    """unused-import shouldn't be emitted for Namespace"""
    cls: "Namespace"
