"""Regression for https://github.com/pylint-dev/pylint/issues/9865."""
# pylint: disable=missing-docstring,too-few-public-methods,unnecessary-lambda-assignment
class C:
    eq = lambda self, y: self == y

def test_lambda_method():
    ret = C().eq(1)
    return ret
