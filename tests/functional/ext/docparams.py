"""Fixture for testing missing documentation in docparams."""


def _private_func(param1):  # [missing-return-doc, missing-return-type-doc]
    if param1:
        raise Exception('Example')
    return param1


def _private_func2(param1):  # [missing-yield-doc, missing-yield-type-doc]
    yield param1
