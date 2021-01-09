"""Fixture for testing missing documentation in docparams."""


def _private_func(param1):
    if param1:
        raise Exception('Example')
    return param1


def _private_func2(param1):
    yield param1
