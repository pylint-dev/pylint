"""Code after a ``typing.NoReturn`` call is unreachable.

https://github.com/pylint-dev/pylint/issues/11271
"""
# pylint: disable=missing-docstring, missing-function-docstring, unused-argument

import typing


def terminate(msg) -> typing.NoReturn:
    raise SystemExit(msg)


def func():
    terminate("done")
    print("unreachable")  # [unreachable]
