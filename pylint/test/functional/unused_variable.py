# pylint: disable=missing-docstring, invalid-name, too-few-public-methods, no-self-use

def test_regression_737():
    import xml # [unused-variable]

def test_regression_923():
    import unittest.case  # [unused-variable]
    import xml as sql # [unused-variable]

def test_unused_with_prepended_underscore():
    _foo = 42
    _ = 24
    __a = 24
    dummy = 24
    _a_ = 42 # [unused-variable]
    __a__ = 24 # [unused-variable]
    __never_used = 42

def test_local_field_prefixed_with_unused_or_ignored():
    flagged_local_field = 42 # [unused-variable]
    unused_local_field = 42
    ignored_local_field = 42


class HasUnusedDunderClass(object):

    def test(self):
        __class__ = 42  # [unused-variable]

    def best(self):
        self.test()


def locals_example_defined_before():
    value = 42  # [possibly-unused-variable]
    return locals()


def locals_example_defined_after():
    local_variables = locals()
    value = 42  # [unused-variable]
    return local_variables


def locals_does_not_account_for_subscopes():
    value = 42  # [unused-variable]

    def some_other_scope():
        return locals()
    return some_other_scope
