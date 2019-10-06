"""Test that a recursion error does not happen

https://github.com/PyCQA/pylint/issues/2463
"""
import os

ABC = os.path.realpath('abc')
DEF = os.path.realpath(ABC + 'def')
GHI = os.path.join(DEF, 'ghi')
