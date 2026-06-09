# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/2821

MagicMock attribute reassigned to lambda should not trigger no-member.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring
from unittest.mock import MagicMock


def test1():
    bigquery = MagicMock()

    def get_table(ds_table):
        return ds_table

    bigquery.get_table = get_table


def test2():
    bigquery = MagicMock()
    bigquery.get_table = lambda x: x
    print(bigquery.get_table(1))
