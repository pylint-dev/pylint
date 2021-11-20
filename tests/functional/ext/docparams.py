"""Fixture for testing missing documentation in docparams."""


def _private_func1(param1):  # [missing-return-doc, missing-return-type-doc]
    """This is a test docstring without returns"""
    return param1


def _private_func2(param1):  # [missing-yield-doc, missing-yield-type-doc]
    """This is a test docstring without yields"""
    yield param1


def _private_func3(param1):  # [missing-raises-doc]
    """This is a test docstring without raises"""
    raise Exception('Example')


def public_func1(param1):  # [missing-any-param-doc]
    """This is a test docstring without params"""
    print(param1)


async def _async_private_func1(param1):  # [missing-return-doc, missing-return-type-doc]
    """This is a test docstring without returns"""
    return param1


async def _async_private_func2(param1):  # [missing-yield-doc, missing-yield-type-doc]
    """This is a test docstring without yields"""
    yield param1


async def _async_private_func3(param1):  # [missing-raises-doc]
    """This is a test docstring without raises"""
    raise Exception('Example')


async def async_public_func1(param1):  # [missing-any-param-doc]
    """This is a test docstring without params"""
    print(param1)
