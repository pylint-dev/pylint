"""Test that a recursion error does not happen

https://github.com/PyCQA/astroid/issues/623
"""
from os import path

FIRST = path.normpath(path.dirname(path.realpath(__file__)))
SECOND = path.normpath(path.abspath(path.join(FIRST, "..")))
THIRD = path.normpath(path.abspath(path.join(SECOND, "..")))
FOURTH = path.join(THIRD)
