# pylint: disable=unused-import,multiple-imports,no-self-use,missing-docstring,invalid-name,too-few-public-methods

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
        import turtle  # [import-outside-toplevel]


def k(flag):
    if flag:
        import tabnanny  # [import-outside-toplevel]


def j():
    from collections import defaultdict # [import-outside-toplevel]


def m():
    from math import sin as sign, cos as cosplay  # [import-outside-toplevel]
