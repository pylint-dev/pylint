# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/4920

'not isinstance() or attr' narrowing should not trigger no-member.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,too-few-public-methods
class ClientResponseError(Exception):
    status: int


def f(exc):
    if not isinstance(exc, ClientResponseError) or exc.status != 404:
        print("x")
    else:
        print("y")
