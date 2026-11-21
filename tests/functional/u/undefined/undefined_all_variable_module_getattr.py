"""A module level ``__getattr__`` (PEP 562) can serve the names listed in ``__all__``.

Other tests for undefined-all-variable in tests/functional/n/names_in__all__.py
"""

__all__ = ["served_lazily", "SERVED_TOO"]


def __getattr__(name):
    if name in __all__:
        return name.lower()
    raise AttributeError(name)
