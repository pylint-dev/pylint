"""PEP 810 restricts where a lazy import may appear."""
# pylint: disable=import-outside-toplevel,missing-function-docstring
# pylint: disable=missing-class-docstring,too-few-public-methods,unused-import
# pylint: disable=using-constant-test,wildcard-import,wrong-import-position
# pylint: disable=redefined-builtin,unused-wildcard-import
lazy import os


def in_function():
    lazy import json  # [invalid-lazy-import]
    return json


class InClass:
    lazy import csv  # [invalid-lazy-import]


try:
    lazy import stat  # [invalid-lazy-import]
except ImportError:
    pass

try:
    pass
except ImportError:
    lazy import gzip  # [invalid-lazy-import]
else:
    lazy import bz2  # [invalid-lazy-import]
finally:
    lazy import lzma  # [invalid-lazy-import]

lazy from math import *  # [invalid-lazy-import]

if os:
    lazy import zlib

for _ in range(1):
    lazy import ast

while os:
    lazy import dis
