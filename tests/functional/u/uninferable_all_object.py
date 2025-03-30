"""Test that non-inferable __all__ variables do not make Pylint crash."""

__all__ = sorted([
    'Dummy',
    'NonExistent',
    'path',
    'func',
    'inner',
    'InnerKlass'])
