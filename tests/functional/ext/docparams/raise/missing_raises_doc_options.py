"""Minimal example where a W9006 message is displayed even if the
accept-no-raise-doc option is set to True.

Requires at least one matching section (`Docstring.matching_sections`).

Taken from https://github.com/pylint-dev/pylint/issues/7208
"""


def w9006issue(dummy: int):
    """Sample function.

    :param dummy: Unused
    """
    raise AssertionError()
