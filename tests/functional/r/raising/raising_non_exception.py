"""The following code should emit a raising-non-exception.

Previously, it didn't, due to a bug in the check for bad-exception-cause,
which prevented further checking on the Raise node.
"""
# pylint: disable=import-error, too-few-public-methods

from missing_module import missing

class Exc:
    """Not an actual exception."""

raise Exc from missing # [raising-non-exception]
