"""unused import"""
# pylint: disable=undefined-all-variable, import-error, too-few-public-methods, missing-docstring,wrong-import-position, multiple-imports
import xml.etree  # [unused-import]
import xml.sax  # [unused-import]
import os.path as test  # [unused-import]
from abc import ABCMeta
from sys import argv as test2  # [unused-import]
from sys import flags  # [unused-import]

# +1:[unused-import,unused-import]
from collections import deque, OrderedDict, Counter
import re, html.parser  # [unused-import]
import six

DATA = Counter()
# pylint: disable=self-assigning-variable
from fake import SomeName, SomeOtherName  # [unused-import]


class SomeClass:
    SomeName = SomeName  # https://bitbucket.org/logilab/pylint/issue/475
    SomeOtherName = 1
    SomeOtherName = SomeOtherName


from never import __all__

# pylint: disable=wrong-import-order,ungrouped-imports,reimported
import typing
from typing import TYPE_CHECKING
import typing as t


if typing.TYPE_CHECKING:
    import collections
if TYPE_CHECKING:
    import itertools
if t.TYPE_CHECKING:
    import xml


example: t.Annotated[str, "Path"] = "/foo/bar"

def get_ordered_dict() -> "collections.OrderedDict":
    return []


def get_itertools_obj() -> "itertools.count":
    return []


def use_html_parser() -> "html.parser.HTMLParser":
    return html.parser.HTMLParser


import os  # [unused-import]
import sys


class NonRegr:
    """???"""

    def __init__(self):
        print("initialized")

    def sys(self):
        """should not get sys from there..."""
        print(self, sys)

    def dummy(self, truc):
        """yo"""
        return self, truc

    def blop(self):
        """yo"""
        print(self, "blip")


if TYPE_CHECKING:
    if sys.version_info >= (3, 6, 2):
        from typing import NoReturn

# Pathological cases
from io import TYPE_CHECKING  # pylint: disable=no-name-in-module
import trace as t
import astroid as typing  # pylint: disable=shadowed-import

TYPE_CHECKING = "red herring"

if TYPE_CHECKING:
    import unittest  # [unused-import]
if t.TYPE_CHECKING:  # pylint: disable=no-member
    import uuid  # [unused-import]
if typing.TYPE_CHECKING:  # pylint: disable=no-member
    import warnings  # [unused-import]
if typing.TYPE_CHECKING_WITH_MAGIC:  # pylint: disable=no-member
    import compileall  # [unused-import]

TYPE_CHECKING = False
if TYPE_CHECKING:
    import zoneinfo


class WithMetaclass(six.with_metaclass(ABCMeta)):
    """Regression test for https://github.com/pylint-dev/pylint/issues/7506.

    Requires six."""


# Regression test for https://github.com/pylint-dev/pylint/issues/3765
# `unused-import` should not be emitted when a type annotation uses quotation marks
from typing import List


class Bee:
    def get_all_classes(self) -> "List[Bee]":
        pass
