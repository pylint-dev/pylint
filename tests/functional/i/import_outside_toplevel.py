# pylint: disable=unused-import,multiple-imports,missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=comparison-of-constants

import abc

if 4 == 5:
    import ast


def f():
    import symtable  # [import-outside-toplevel]


def g():
    import os, sys  # [import-outside-toplevel]


def h():
    import time as thyme  # [import-outside-toplevel]


def i():
    import random as rand, socket as sock  # [import-outside-toplevel]


class C:
    import tokenize  # [import-outside-toplevel]

    def j(self):
        import trace  # [import-outside-toplevel]


def k(flag):
    if flag:
        import tabnanny  # [import-outside-toplevel]


def j():
    from collections import defaultdict # [import-outside-toplevel]


def m():
    from math import sin as sign, cos as cosplay  # [import-outside-toplevel]


# Test allow-any-import-level setting
def n():
    import astroid

def o():
    import notastroid  # [import-error, import-outside-toplevel]
