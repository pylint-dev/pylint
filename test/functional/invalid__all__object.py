"""Test that non-inferable __all__ variables do not make Pylint crash."""

__all__ = [SomeUndefinedName]  # [undefined-variable]
