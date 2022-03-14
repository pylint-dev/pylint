"""Tests for assign-to-new-keyword"""
# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods, function-redefined

async = "foo"  # [assign-to-new-keyword]
await = "bar"  # [assign-to-new-keyword]


def async():  # [assign-to-new-keyword]
    pass


class async:  # [assign-to-new-keyword]
    pass
