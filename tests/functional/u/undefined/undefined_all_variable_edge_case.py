"""Edge case: __all__ exists in module's locals, but cannot be inferred.

Other tests for undefined-all-variable in tests/functional/n/names_in__all__.py"""

__all__ += []  # [undefined-variable]
