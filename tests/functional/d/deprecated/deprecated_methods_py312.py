"""Test deprecated methods from Python 3.12."""
# pylint: disable=missing-function-docstring

import datetime


def naive_now():
    return datetime.datetime.utcnow()  # [deprecated-method]


def naive_from_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)  # [deprecated-method]
