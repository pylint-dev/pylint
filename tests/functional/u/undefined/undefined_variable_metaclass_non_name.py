"""Regression test for a crash in the variables checker when a class uses a
metaclass whose attribute-access chain does not bottom out at a ``Name``.

For ``metaclass=None._`` the metaclass node is an ``Attribute`` whose ``expr``
is a ``Const``; walking the ``.expr`` chain looking for a ``Name`` used to
crash with an ``AttributeError``.

https://github.com/pylint-dev/pylint/issues/11030
"""
# pylint: disable=too-few-public-methods,missing-class-docstring


class C(metaclass=None._):
    pass
