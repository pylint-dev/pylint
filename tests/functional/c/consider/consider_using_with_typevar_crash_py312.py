"""Crash regression for ``consider-using-with`` with PEP 695 type parameters.

Calling a type parameter inferred as ``nodes.TypeVar`` must not crash when
checking whether the callee is a known context-manager factory.

https://github.com/pylint-dev/pylint/issues/11058
"""

# pylint: disable=invalid-name

type T[U] = None
_ = U()  # [not-callable]
