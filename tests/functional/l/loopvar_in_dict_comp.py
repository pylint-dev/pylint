"""Tests for loopvar-in-closure."""


def bad_case():
    """Loop variable from dict comprehension."""
    return {x: lambda: x for x in range(10)} # [cell-var-from-loop]
