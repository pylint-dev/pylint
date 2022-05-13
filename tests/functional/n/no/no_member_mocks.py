""" Test that Mock objects don't raise a no-member. See issue #2821 """

# pylint: disable=missing-function-docstring
from unittest.mock import Mock


def real_no_member():
    exc = BaseException()
    exc.no_member()  # [no-member]


def mock_function_override():
    bigquery = Mock()

    def get_table(ds_table):
        return ds_table

    bigquery.get_table = get_table


def mock_function_return_value():
    bigquery = Mock()
    destination_table = bigquery.get_table.return_value
    destination_table.num_rows = 0
