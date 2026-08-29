"""Regression test for https://github.com/pylint-dev/pylint/issues/11071.

A class whose ``metaclass=`` argument resolves to a plain ``FunctionDef``
(rather than a ``ClassDef``) crashed the typecheck checker when looking up
``__call__`` on the metaclass via ``local_attr``.
"""

# pylint: disable=missing-docstring,too-few-public-methods,invalid-metaclass


def fn():
    pass


class C(metaclass=fn):
    pass


C()
