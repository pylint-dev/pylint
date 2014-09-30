"""
Check for indexing exceptions.
"""
# pylint: disable=import-error
__revision__ = 0

from unknown import ExtensionException

class SubException(IndexError):
    """ empty """

_ = IndexError("test")[0]
_ = ZeroDivisionError("error")[0]
_ = ExtensionException("error")[0]
_ = SubException("error")[1]
