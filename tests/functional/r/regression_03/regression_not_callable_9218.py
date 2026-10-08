"""Regression test for https://github.com/pylint-dev/pylint/issues/9218.

``torch`` wraps its functions with ``_add_docstr``, which its stubs declare with
a body that is only ``...``. The call used to be inferred as returning ``None``,
so every wrapped function was reported as not callable.
"""

# pylint: disable=missing-function-docstring,unused-argument,assignment-from-no-return

from typing import TypeVar

T = TypeVar("T")


def _add_docstr(obj: T, doc_obj: str) -> T: ...


def _one_hot(tensor, num_classes=-1):
    return [tensor, num_classes]


one_hot = _add_docstr(_one_hot, "one_hot(tensor, num_classes=-1) -> LongTensor")
one_hot([0, 1, 2], num_classes=4)
