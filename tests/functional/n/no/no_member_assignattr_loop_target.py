"""Regression test for https://github.com/pylint-dev/pylint/issues/11356.

Metaclass attribute lookup could fail to infer an ``AssignAttr`` bound by a for-loop
target and raise ``InferenceError``, which was not handled alongside ``NotFoundError``.
"""
# pylint: disable=too-few-public-methods,undefined-variable
from collections.abc import GenericAlias


class C:
    """Attribute is looked up here before the loop below binds it elsewhere."""


x = C.a

for GenericAlias.a in _:
    pass
