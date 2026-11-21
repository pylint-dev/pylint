"""Package whose ``__all__`` does not list all of its public names."""

import os

__all__ = ["exported"]


def exported() -> int:
    """Return a value, using the import above so that it is not unused."""
    return os.getpid()
