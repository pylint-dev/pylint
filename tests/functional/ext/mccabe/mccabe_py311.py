"""Checks for too-complex with syntax requiring Python 3.11 or newer."""

# pylint: disable=missing-docstring


def exception_groups(shielded):  # [too-complex]
    """McCabe rating: 1

    The mccabe library predates ``except*`` and does not count it."""
    result = "none"
    try:
        shielded()
    except* TypeError:
        result = "type"
    except* ValueError:
        result = "value"
    return result
