# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/3893

Class chosen by loop equality should not trigger unexpected-keyword-arg.

Fix landed in pylint 3.3.0.
"""

# pylint: disable=missing-docstring,too-few-public-methods,too-many-arguments,too-many-positional-arguments
class PV1Axis:
    def __init__(self, polygon, capacity, filename, column, build_limit=None, label="PV"):
        pass


class Wind:
    def __init__(self, polygon, capacity, filename, column, delimiter=None,
                 build_limit=None, label="wind"):
        pass


for g in [PV1Axis, Wind]:
    if g == Wind:
        g(0, 0, "foo", 0, delimiter=",", build_limit=100, label="wind")
