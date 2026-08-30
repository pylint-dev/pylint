# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/9159

``typing.Self`` return type of a ``classmethod`` override should narrow to
the subclass when chained off ``B.f1().f2()``.

Fix landed in astroid between 4.0.4 and 4.2.0b3; first clean on
pylint 4.1.0-dev0 (bug present on pylint 4.0.5 + astroid 4.0.4).
"""

# pylint: disable=missing-docstring,too-few-public-methods
import typing


class A:
    @classmethod
    def f1(cls) -> typing.Self:
        return cls()


class B(A):
    @classmethod
    def f1(cls) -> typing.Self:
        return super(B, cls).f1()

    def f2(self):
        pass


B.f1().f2()
