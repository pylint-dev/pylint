"""Test of unused import warnings while type hinting"""
# pylint: disable=wrong-import-position, unused-argument, import-error, missing-docstring
from fake import SomeName  # [unused-import]

# following should be ok
from fake import OtherName
def my_method(attribute: OtherName):
    pass

from fake import AnotherName
def another_method(attribute: 'AnotherName'):
    pass
